/**
 * Cloudflare Pages Function für Kontaktformular
 * Sendet E-Mails über Resend API mit Spam-Schutz
 *
 * Features:
 * - E-Mail-Versand über Resend API
 * - Turnstile CAPTCHA (optional, mit Fallback für Adblocker)
 * - Math-Captcha als Fallback wenn Turnstile geblockt
 * - KV Backup: Alle Anfragen werden gespeichert (auch wenn E-Mail fehlschlägt)
 * - Mehrschichtiger Spam-Schutz (Honeypot, Rate Limiting, Bot Detection)
 *
 * Setup:
 * 1. Resend Account: https://resend.com → API Key erstellen
 * 2. Cloudflare Pages Environment Variables:
 *    - RESEND_API_KEY: Dein Resend API Key
 *    - TURNSTILE_SECRET_KEY: Cloudflare Turnstile Secret Key (optional)
 *
 * 3. Cloudflare KV Namespace (WICHTIG für Backup!):
 *    - Workers & Pages → KV → Create namespace: "CONTACT_BACKUP_KV"
 *    - Pages Projekt → Settings → Functions → KV Namespace Bindings
 *    - Variable name: CONTACT_BACKUP_KV
 *    - Namespace: CONTACT_BACKUP_KV
 *
 * E-Mails werden an beide Adressen gesendet:
 *    - info@kost-sicherheitstechnik.de
 *    - info@graphiks.de
 */

// Rate limiting configuration
const RATE_LIMIT_WINDOW = 15 * 60; // 15 minutes in seconds
const RATE_LIMIT_MAX = 5; // Max 5 submissions per 15 minutes per IP (erhöht von 3)

// Spam keywords to filter
const SPAM_KEYWORDS = [
  'seo', 'backlink', 'günstige', 'billige',
  'bitcoin', 'crypto', 'investment', 'kredit', 'darlehen',
  'viagra', 'cialis', 'casino', 'poker', 'gewinn',
  'lottery', 'winner', 'prize', 'click here', 'limited time',
  'free money', 'work from home', 'make money', 'get rich',
  'nigerian prince', 'lottery winner', 'inheritance',
  'act now', 'limited offer', 'guaranteed', 'no risk'
];

// Known bot user agents
const BOT_USER_AGENTS = [
  'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget',
  'python-requests', 'java/', 'php/', 'perl', 'ruby',
  'httpie', 'postman', 'insomnia'
];

/**
 * Get client IP from Cloudflare headers
 */
function getClientIP(request) {
  const cfConnectingIP = request.headers.get('CF-Connecting-IP');
  const xForwardedFor = request.headers.get('X-Forwarded-For');
  return cfConnectingIP || xForwardedFor?.split(',')[0]?.trim() || 'unknown';
}

/**
 * Generate a unique ID for contact submissions
 */
function generateContactId() {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 8);
  return `contact_${timestamp}_${random}`;
}

/**
 * Save contact submission to KV as backup
 * This ensures no contact is lost even if email fails
 */
async function saveContactToKV(kv, contactData) {
  if (!kv) {
    console.warn('KV not available for backup');
    return { saved: false, error: 'KV not configured' };
  }

  try {
    const contactId = generateContactId();
    const timestamp = new Date().toISOString();

    const entry = {
      id: contactId,
      timestamp,
      ...contactData,
      status: 'pending' // Can be updated to 'processed' later
    };

    // Store with 90-day expiration (can be retrieved via Cloudflare Dashboard or API)
    await kv.put(contactId, JSON.stringify(entry), {
      expirationTtl: 90 * 24 * 60 * 60 // 90 days
    });

    // Also maintain an index of recent contacts for easy retrieval
    const indexKey = `index_${timestamp.slice(0, 10)}`; // Daily index
    let dailyIndex = await kv.get(indexKey, { type: 'json' }) || [];
    dailyIndex.push(contactId);
    await kv.put(indexKey, JSON.stringify(dailyIndex), {
      expirationTtl: 90 * 24 * 60 * 60
    });

    console.log('Contact saved to KV:', contactId);
    return { saved: true, contactId };
  } catch (error) {
    console.error('Failed to save contact to KV:', error);
    return { saved: false, error: error.message };
  }
}

/**
 * Check rate limiting using Cloudflare KV
 */
async function checkRateLimit(ip, kv = null) {
  const key = `rate_limit:${ip}`;
  const now = Math.floor(Date.now() / 1000);

  if (kv) {
    try {
      const stored = await kv.get(key, { type: 'json' });

      if (!stored) {
        await kv.put(key, JSON.stringify({ count: 1, firstRequest: now }), {
          expirationTtl: RATE_LIMIT_WINDOW
        });
        return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
      }

      const elapsed = now - stored.firstRequest;

      if (elapsed >= RATE_LIMIT_WINDOW) {
        await kv.put(key, JSON.stringify({ count: 1, firstRequest: now }), {
          expirationTtl: RATE_LIMIT_WINDOW
        });
        return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
      }

      if (stored.count >= RATE_LIMIT_MAX) {
        const waitTime = Math.ceil((RATE_LIMIT_WINDOW - elapsed) / 60);
        return { allowed: false, waitTime };
      }

      stored.count++;
      await kv.put(key, JSON.stringify(stored), {
        expirationTtl: RATE_LIMIT_WINDOW - elapsed
      });

      return { allowed: true, remaining: RATE_LIMIT_MAX - stored.count };
    } catch (error) {
      console.error('KV rate limit error:', error);
    }
  }

  // Fallback: Allow if KV not available (rely on other spam protection)
  return { allowed: true, remaining: RATE_LIMIT_MAX };
}

/**
 * Verify Cloudflare Turnstile token
 */
async function verifyTurnstile(token, secretKey, clientIP) {
  if (!secretKey || !token) {
    return { success: false, error: 'No token provided', skipped: true };
  }

  try {
    const response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        secret: secretKey,
        response: token,
        remoteip: clientIP,
      }),
    });

    const data = await response.json();
    return { success: data.success === true, error: data['error-codes'], skipped: false };
  } catch (error) {
    console.error('Turnstile verification error:', error);
    return { success: false, error: 'Verification request failed', skipped: false };
  }
}

/**
 * Verify math captcha answer
 */
function verifyMathCaptcha(answer, expectedAnswer) {
  if (!answer || !expectedAnswer) {
    return false;
  }
  // Compare as strings to handle both number and string inputs
  return String(answer).trim() === String(expectedAnswer).trim();
}

/**
 * Check for spam keywords
 */
function containsSpamKeywords(text) {
  const lowerText = text.toLowerCase();
  return SPAM_KEYWORDS.some(keyword => lowerText.includes(keyword));
}

/**
 * Check if message contains URLs
 */
function containsUrls(text) {
  const urlRegex = /https?:\/\/[^\s]+|www\.[^\s]+/gi;
  return urlRegex.test(text);
}

/**
 * Check if user agent is a known bot
 */
function isBotUserAgent(userAgent) {
  if (!userAgent) return true;

  const lowerUA = userAgent.toLowerCase();

  if (BOT_USER_AGENTS.some(bot => lowerUA.includes(bot))) {
    return true;
  }

  // Must have some browser signature
  const legitimateBrowsers = ['mozilla', 'chrome', 'safari', 'firefox', 'edge', 'opera'];
  if (!legitimateBrowsers.some(browser => lowerUA.includes(browser))) {
    return true;
  }

  return false;
}

/**
 * Check for timing-based bot detection
 */
async function checkSubmissionTiming(ip, kv = null) {
  if (!kv) return { suspicious: false };

  const timingKey = `timing:${ip}`;
  const now = Date.now();

  try {
    const stored = await kv.get(timingKey, { type: 'json' });

    if (stored && stored.lastSubmission) {
      const timeSinceLastSubmission = now - stored.lastSubmission;
      if (timeSinceLastSubmission < 3000) { // 3 seconds
        return { suspicious: true, reason: 'Too fast' };
      }
    }

    await kv.put(timingKey, JSON.stringify({ lastSubmission: now }), {
      expirationTtl: 60
    });
  } catch (error) {
    console.error('Timing check error:', error);
  }

  return { suspicious: false };
}

// Helper: HTML-Escape
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  };
  return String(text).replace(/[&<>"']/g, (m) => map[m]);
}

export async function onRequestPost(context) {
  const { request, env } = context;

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  // Get KV namespaces
  const rateLimitKV = env.RATE_LIMIT_KV || null;
  const contactBackupKV = env.CONTACT_BACKUP_KV || env.RATE_LIMIT_KV || null; // Fallback to rate limit KV

  try {
    const clientIP = getClientIP(request);
    const userAgent = request.headers.get('User-Agent') || '';

    // === BOT DETECTION ===
    if (isBotUserAgent(userAgent)) {
      console.warn('Bot detected:', userAgent, 'IP:', clientIP);
      // Fake success to confuse bots
      return new Response(
        JSON.stringify({ success: true, message: 'Ihre Nachricht wurde erfolgreich gesendet.' }),
        { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // === TIMING CHECK ===
    const timingCheck = await checkSubmissionTiming(clientIP, rateLimitKV);
    if (timingCheck.suspicious) {
      console.warn('Suspicious timing:', clientIP);
      return new Response(
        JSON.stringify({ success: true, message: 'Ihre Nachricht wurde erfolgreich gesendet.' }),
        { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // === RATE LIMITING ===
    const rateLimit = await checkRateLimit(clientIP, rateLimitKV);
    if (!rateLimit.allowed) {
      return new Response(
        JSON.stringify({ error: `Zu viele Anfragen. Bitte warten Sie ${rateLimit.waitTime} Minuten.` }),
        { status: 429, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // === PARSE FORM DATA ===
    const formData = await request.formData();
    const name = formData.get('name')?.trim();
    const phone = formData.get('phone')?.trim();
    const email = formData.get('email')?.trim();
    const message = formData.get('message')?.trim();
    const website = formData.get('website'); // Honeypot
    const turnstileToken = formData.get('cf-turnstile-response');
    const mathAnswer = formData.get('mathAnswer');
    const mathExpected = formData.get('mathExpected');
    const usedFallback = formData.get('usedFallback') === 'true';

    // === VALIDATION ===
    if (!name || !phone || !email || !message) {
      return new Response(
        JSON.stringify({ error: 'Bitte füllen Sie alle Felder aus.' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // Honeypot check
    if (website && website.trim() !== '') {
      console.warn('Honeypot triggered:', clientIP);
      return new Response(
        JSON.stringify({ success: true, message: 'Ihre Nachricht wurde erfolgreich gesendet.' }),
        { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return new Response(
        JSON.stringify({ error: 'Bitte geben Sie eine gültige E-Mail-Adresse ein.' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // Message length
    if (message.length < 10) {
      return new Response(
        JSON.stringify({ error: 'Ihre Nachricht ist zu kurz (min. 10 Zeichen).' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    if (message.length > 5000) {
      return new Response(
        JSON.stringify({ error: 'Ihre Nachricht ist zu lang (max. 5000 Zeichen).' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // Spam keyword check
    if (containsSpamKeywords(message) || containsSpamKeywords(name)) {
      console.warn('Spam keywords detected:', clientIP);
      return new Response(
        JSON.stringify({ error: 'Ihre Nachricht enthält unzulässige Inhalte.' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // URL check
    if (containsUrls(message)) {
      console.warn('URL in message:', clientIP);
      return new Response(
        JSON.stringify({ error: 'Bitte senden Sie keine Links. Kontaktieren Sie uns direkt.' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // === CAPTCHA VERIFICATION ===
    let captchaMethod = 'none';
    let captchaValid = false;

    const turnstileSecretKey = env.TURNSTILE_SECRET_KEY;

    // Try Turnstile first (if token provided)
    if (turnstileToken && turnstileSecretKey) {
      const turnstileResult = await verifyTurnstile(turnstileToken, turnstileSecretKey, clientIP);
      if (turnstileResult.success) {
        captchaMethod = 'turnstile';
        captchaValid = true;
      } else {
        console.warn('Turnstile failed:', clientIP, turnstileResult.error);
      }
    }

    // Fallback to Math Captcha (if Turnstile not used/failed)
    if (!captchaValid && usedFallback && mathAnswer && mathExpected) {
      if (verifyMathCaptcha(mathAnswer, mathExpected)) {
        captchaMethod = 'math';
        captchaValid = true;
      } else {
        console.warn('Math captcha failed:', clientIP);
        return new Response(
          JSON.stringify({ error: 'Die Rechenaufgabe wurde falsch beantwortet. Bitte versuchen Sie es erneut.' }),
          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
    }

    // If no captcha method succeeded but Turnstile is configured, reject
    // (This prevents bypass by not sending any captcha data)
    if (!captchaValid && turnstileSecretKey && !usedFallback) {
      return new Response(
        JSON.stringify({ error: 'Bitte bestätigen Sie, dass Sie kein Roboter sind.' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // === PREPARE CONTACT DATA ===
    const contactData = {
      name,
      phone,
      email,
      message,
      ip: clientIP,
      userAgent: userAgent.substring(0, 200), // Truncate for storage
      captchaMethod,
      source: 'website'
    };

    // === SAVE TO KV BACKUP (ALWAYS, BEFORE EMAIL) ===
    const kvResult = await saveContactToKV(contactBackupKV, contactData);

    // === SEND EMAIL ===
    const resendApiKey = env.RESEND_API_KEY;
    const contactEmails = ['info@kost-sicherheitstechnik.de', 'info@graphiks.de'];

    let emailSent = false;
    let emailError = null;

    if (resendApiKey) {
      try {
        const emailResponse = await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${resendApiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            from: 'Website Kontaktformular <noreply@mail.kost-sicherheitstechnik.de>',
            to: contactEmails,
            replyTo: email,
            subject: `Neue Anfrage von ${name} - KOST Sicherheitstechnik`,
            html: `
              <!DOCTYPE html>
              <html>
                <head>
                  <meta charset="UTF-8">
                  <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: #FA0016; color: white; padding: 20px; text-align: center; }
                    .content { background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }
                    .field { margin-bottom: 15px; }
                    .label { font-weight: bold; color: #1d1d1f; }
                    .value { margin-top: 5px; color: #6e6e73; }
                    .message-box { background: white; padding: 15px; border-left: 4px solid #FA0016; margin-top: 10px; }
                    .meta { font-size: 11px; color: #999; margin-top: 20px; padding-top: 10px; border-top: 1px solid #eee; }
                  </style>
                </head>
                <body>
                  <div class="container">
                    <div class="header">
                      <h1>Neue Anfrage über Website</h1>
                    </div>
                    <div class="content">
                      <div class="field">
                        <div class="label">Name:</div>
                        <div class="value">${escapeHtml(name)}</div>
                      </div>
                      <div class="field">
                        <div class="label">Telefon:</div>
                        <div class="value">${escapeHtml(phone)}</div>
                      </div>
                      <div class="field">
                        <div class="label">E-Mail:</div>
                        <div class="value">${escapeHtml(email)}</div>
                      </div>
                      <div class="field">
                        <div class="label">Nachricht:</div>
                        <div class="message-box">${escapeHtml(message).replace(/\n/g, '<br>')}</div>
                      </div>
                      <div class="meta">
                        Verifizierung: ${captchaMethod} | Backup-ID: ${kvResult.contactId || 'nicht gespeichert'}
                      </div>
                    </div>
                  </div>
                </body>
              </html>
            `,
            text: `Neue Anfrage über Website\n\nName: ${name}\nTelefon: ${phone}\nE-Mail: ${email}\n\nNachricht:\n${message}\n\n---\nVerifizierung: ${captchaMethod}\nBackup-ID: ${kvResult.contactId || 'nicht gespeichert'}`,
          }),
        });

        if (emailResponse.ok) {
          emailSent = true;
        } else {
          const errorData = await emailResponse.text();
          emailError = errorData;
          console.error('Resend error:', emailResponse.status, errorData);
        }
      } catch (error) {
        emailError = error.message;
        console.error('Email send error:', error);
      }
    } else {
      emailError = 'RESEND_API_KEY nicht konfiguriert';
      console.error('RESEND_API_KEY missing');
    }

    // === RESPONSE ===
    // Always return success to user if data was saved (even if email failed)
    if (kvResult.saved || emailSent) {
      return new Response(
        JSON.stringify({
          success: true,
          message: 'Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns kurzfristig bei Ihnen.',
          backupId: kvResult.contactId
        }),
        { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // Both failed - this is critical
    console.error('CRITICAL: Both email and KV backup failed!', { emailError, kvError: kvResult.error });
    return new Response(
      JSON.stringify({ error: 'Ein technischer Fehler ist aufgetreten. Bitte kontaktieren Sie uns telefonisch.' }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );

  } catch (error) {
    console.error('Contact form error:', error);
    return new Response(
      JSON.stringify({ error: 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.' }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
}
