/**
 * Cloudflare Pages Function für Kontaktformular
 * Sendet E-Mails über Resend API mit Spam-Schutz
 * 
 * Setup:
 * 1. Resend Account erstellen: https://resend.com
 * 2. API Key erstellen
 * 3. In Cloudflare Pages: Settings → Environment variables
 *    - RESEND_API_KEY: Dein Resend API Key
 *    - TURNSTILE_SECRET_KEY: Cloudflare Turnstile Secret Key (optional, aber empfohlen)
 * 
 * 4. Cloudflare KV für Rate Limiting (optional, aber empfohlen):
 *    - Workers & Pages → KV → Create namespace: "RATE_LIMIT_KV"
 *    - Pages Projekt → Settings → Functions → KV Namespace Bindings
 *    - Variable name: RATE_LIMIT_KV
 *    - Namespace: RATE_LIMIT_KV
 * 
 * E-Mails werden an beide Adressen gesendet:
 *    - info@kost-sicherheitstechnik.de
 *    - info@graphiks.de
 */

// Rate limiting configuration
const RATE_LIMIT_WINDOW = 15 * 60; // 15 minutes in seconds (for KV TTL)
const RATE_LIMIT_MAX = 3; // Max 3 submissions per 15 minutes per IP

// Spam keywords to filter
const SPAM_KEYWORDS = [
  'cloudflare', 'seo', 'backlink', 'günstige', 'billige', 'kostenlos',
  'bitcoin', 'crypto', 'investment', 'kredit', 'darlehen',
  'viagra', 'cialis', 'casino', 'poker', 'gewinn',
  'lottery', 'winner', 'prize', 'click here', 'limited time',
  'free money', 'work from home', 'make money', 'get rich',
  'nigerian prince', 'lottery winner', 'inheritance', 'urgent',
  'act now', 'limited offer', 'guaranteed', 'no risk'
];

// Known bot user agents
const BOT_USER_AGENTS = [
  'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget',
  'python', 'java', 'php', 'perl', 'ruby', 'go-http',
  'httpie', 'postman', 'insomnia', 'apache', 'nginx'
];

// Suspicious user agents (often used by spam bots)
const SUSPICIOUS_USER_AGENTS = [
  'mozilla/4.0', 'mozilla/3.0', 'mozilla/2.0', // Old browser versions
  'windows 95', 'windows 98', 'windows me', // Old OS
  'internet explorer 6', 'internet explorer 5'
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
 * Check rate limiting using Cloudflare KV (persistent) or fallback to in-memory
 * @param {string} ip - Client IP address
 * @param {object} kv - Cloudflare KV namespace (optional)
 * @returns {Promise<{allowed: boolean, waitTime?: number, remaining?: number}>}
 */
async function checkRateLimit(ip, kv = null) {
  const key = `rate_limit:${ip}`;
  const now = Math.floor(Date.now() / 1000); // Current time in seconds
  
  // Try KV first if available
  if (kv) {
    try {
      const stored = await kv.get(key, { type: 'json' });
      
      if (!stored) {
        // First request from this IP
        await kv.put(key, JSON.stringify({ count: 1, firstRequest: now }), {
          expirationTtl: RATE_LIMIT_WINDOW
        });
        return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
      }
      
      const elapsed = now - stored.firstRequest;
      
      if (elapsed >= RATE_LIMIT_WINDOW) {
        // Window expired, reset
        await kv.put(key, JSON.stringify({ count: 1, firstRequest: now }), {
          expirationTtl: RATE_LIMIT_WINDOW
        });
        return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
      }
      
      if (stored.count >= RATE_LIMIT_MAX) {
        // Rate limit exceeded
        const waitTime = Math.ceil((RATE_LIMIT_WINDOW - elapsed) / 60);
        return { allowed: false, waitTime };
      }
      
      // Increment count
      stored.count++;
      await kv.put(key, JSON.stringify(stored), {
        expirationTtl: RATE_LIMIT_WINDOW - elapsed
      });
      
      return { allowed: true, remaining: RATE_LIMIT_MAX - stored.count };
    } catch (error) {
      console.error('KV rate limit error:', error);
      // Fall through to in-memory fallback
    }
  }
  
  // Fallback: In-memory rate limiting (if KV not available)
  if (!globalThis.rateLimitStore) {
    globalThis.rateLimitStore = new Map();
  }
  
  const entry = globalThis.rateLimitStore.get(key);
  const nowMs = Date.now();
  
  if (!entry) {
    globalThis.rateLimitStore.set(key, { count: 1, resetAt: nowMs + (RATE_LIMIT_WINDOW * 1000) });
    return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
  }
  
  if (nowMs > entry.resetAt) {
    globalThis.rateLimitStore.set(key, { count: 1, resetAt: nowMs + (RATE_LIMIT_WINDOW * 1000) });
    return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
  }
  
  if (entry.count >= RATE_LIMIT_MAX) {
    const waitTime = Math.ceil((entry.resetAt - nowMs) / 1000 / 60);
    return { allowed: false, waitTime };
  }
  
  entry.count++;
  globalThis.rateLimitStore.set(key, entry);
  return { allowed: true, remaining: RATE_LIMIT_MAX - entry.count };
}

/**
 * Verify Cloudflare Turnstile token
 */
async function verifyTurnstile(token, secretKey, clientIP) {
  if (!secretKey || !token) {
    return { success: false, error: 'Turnstile not configured' };
  }

  try {
    const response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        secret: secretKey,
        response: token,
        remoteip: clientIP,
      }),
    });

    const data = await response.json();
    return { success: data.success === true, error: data['error-codes'] };
  } catch (error) {
    console.error('Turnstile verification error:', error);
    return { success: false, error: 'Verification failed' };
  }
}

/**
 * Check for spam keywords in message
 */
function containsSpamKeywords(text) {
  const lowerText = text.toLowerCase();
  return SPAM_KEYWORDS.some(keyword => lowerText.includes(keyword));
}

/**
 * Check if message contains URLs (potential spam indicator)
 */
function containsUrls(text) {
  const urlRegex = /https?:\/\/[^\s]+|www\.[^\s]+/gi;
  return urlRegex.test(text);
}

/**
 * Check if user agent is a known bot
 */
function isBotUserAgent(userAgent) {
  if (!userAgent) return true; // No user agent = likely bot
  
  const lowerUA = userAgent.toLowerCase();
  
  // Check for known bots
  if (BOT_USER_AGENTS.some(bot => lowerUA.includes(bot))) {
    return true;
  }
  
  // Check for suspicious user agents
  if (SUSPICIOUS_USER_AGENTS.some(suspicious => lowerUA.includes(suspicious))) {
    return true;
  }
  
  // Check for legitimate browsers (if none found, might be bot)
  const legitimateBrowsers = ['mozilla', 'chrome', 'safari', 'firefox', 'edge', 'opera'];
  if (!legitimateBrowsers.some(browser => lowerUA.includes(browser))) {
    return true; // No legitimate browser signature
  }
  
  return false;
}

/**
 * Check if request has suspicious headers (missing or invalid)
 */
function hasSuspiciousHeaders(request) {
  const userAgent = request.headers.get('User-Agent');
  const referer = request.headers.get('Referer');
  const origin = request.headers.get('Origin');
  const accept = request.headers.get('Accept');
  
  // Missing User-Agent
  if (!userAgent || userAgent.trim() === '') {
    return true;
  }
  
  // Missing Accept header (legitimate browsers always send this)
  if (!accept || !accept.includes('text/html') && !accept.includes('application/json')) {
    return true;
  }
  
  // Check if Referer/Origin matches expected domain
  const expectedDomain = 'kost-sicherheitstechnik.de';
  if (referer && !referer.includes(expectedDomain) && !referer.includes('localhost')) {
    // Referer from different domain might be suspicious
    // But allow it for now (could be legitimate external link)
  }
  
  return false;
}

/**
 * Check for timing-based bot detection (too fast submission)
 * This requires storing submission time per IP
 */
async function checkSubmissionTiming(ip, kv = null) {
  const timingKey = `submission_timing:${ip}`;
  const now = Date.now();
  
  if (kv) {
    try {
      const stored = await kv.get(timingKey, { type: 'json' });
      
      if (stored && stored.lastSubmission) {
        const timeSinceLastSubmission = now - stored.lastSubmission;
        // If submission is less than 2 seconds after last, it's likely a bot
        if (timeSinceLastSubmission < 2000) {
          return { suspicious: true, reason: 'Too fast submission' };
        }
      }
      
      // Store current submission time
      await kv.put(timingKey, JSON.stringify({ lastSubmission: now }), {
        expirationTtl: 60 // Store for 1 minute
      });
    } catch (error) {
      console.error('Timing check error:', error);
    }
  }
  
  return { suspicious: false };
}

export async function onRequestPost(context) {
  const { request, env } = context;
  
  // CORS Headers für Preflight
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  // Handle OPTIONS (CORS Preflight)
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    // Get client IP for rate limiting and Turnstile
    const clientIP = getClientIP(request);
    
    // Get KV namespace if available (bound in Cloudflare Pages settings)
    const kv = env.RATE_LIMIT_KV || null;

    // === BOT DETECTION CHECKS ===
    
    // 1. User-Agent check
    const userAgent = request.headers.get('User-Agent') || '';
    if (isBotUserAgent(userAgent)) {
      console.warn('Bot user agent detected:', userAgent, 'IP:', clientIP);
      // Return success to bot to prevent them from knowing they were caught
      return new Response(
        JSON.stringify({ 
          success: true, 
          message: 'Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns kurzfristig bei Ihnen.' 
        }),
        {
          status: 200,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }
    
    // 2. Suspicious headers check
    if (hasSuspiciousHeaders(request)) {
      console.warn('Suspicious headers detected for IP:', clientIP);
      return new Response(
        JSON.stringify({ 
          success: true, 
          message: 'Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns kurzfristig bei Ihnen.' 
        }),
        {
          status: 200,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }
    
    // 3. Timing-based bot detection
    const timingCheck = await checkSubmissionTiming(clientIP, kv);
    if (timingCheck.suspicious) {
      console.warn('Suspicious timing detected for IP:', clientIP, timingCheck.reason);
      return new Response(
        JSON.stringify({ 
          success: true, 
          message: 'Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns kurzfristig bei Ihnen.' 
        }),
        {
          status: 200,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }
    
    // 4. Rate limiting check (uses KV if available, falls back to in-memory)
    const rateLimit = await checkRateLimit(clientIP, kv);
    if (!rateLimit.allowed) {
      return new Response(
        JSON.stringify({ 
          error: `Zu viele Anfragen. Bitte versuchen Sie es in ${rateLimit.waitTime} Minuten erneut.` 
        }),
        {
          status: 429,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Formular-Daten parsen
    const formData = await request.formData();
    const name = formData.get('name');
    const phone = formData.get('phone');
    const email = formData.get('email');
    const message = formData.get('message');
    const website = formData.get('website'); // Honeypot field
    const turnstileToken = formData.get('cf-turnstile-response'); // Turnstile token

    // Validierung
    if (!name || !phone || !email || !message) {
      return new Response(
        JSON.stringify({ error: 'Alle Felder sind erforderlich' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Honeypot check - if website field is filled, it's a bot
    if (website && website.trim() !== '') {
      console.warn('Honeypot triggered for IP:', clientIP);
      // Return success to bot to prevent them from knowing they were caught
      return new Response(
        JSON.stringify({ 
          success: true, 
          message: 'Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns kurzfristig bei Ihnen.' 
        }),
        {
          status: 200,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Email-Validierung
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return new Response(
        JSON.stringify({ error: 'Ungültige E-Mail-Adresse' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Enhanced validation - message length checks
    if (message.length < 10) {
      return new Response(
        JSON.stringify({ error: 'Bitte geben Sie eine aussagekräftige Nachricht ein (mindestens 10 Zeichen).' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    if (message.length > 5000) {
      return new Response(
        JSON.stringify({ error: 'Ihre Nachricht ist zu lang. Bitte fassen Sie sich kürzer (max. 5000 Zeichen).' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Spam keyword check
    if (containsSpamKeywords(message)) {
      console.warn('Spam keywords detected for IP:', clientIP);
      return new Response(
        JSON.stringify({ error: 'Ihre Nachricht enthält unzulässige Inhalte.' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // URL check - reject if message contains URLs (likely spam)
    if (containsUrls(message)) {
      console.warn('URL detected in message for IP:', clientIP);
      return new Response(
        JSON.stringify({ error: 'Bitte senden Sie keine Links in Ihrer Nachricht. Kontaktieren Sie uns telefonisch oder per E-Mail.' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Turnstile verification (if configured)
    const turnstileSecretKey = env.TURNSTILE_SECRET_KEY;
    if (turnstileSecretKey) {
      const turnstileVerification = await verifyTurnstile(turnstileToken, turnstileSecretKey, clientIP);
      if (!turnstileVerification.success) {
        console.warn('Turnstile verification failed for IP:', clientIP, turnstileVerification.error);
        return new Response(
          JSON.stringify({ error: 'Verifizierung fehlgeschlagen. Bitte versuchen Sie es erneut.' }),
          {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          }
        );
      }
    }

    // Resend API Key aus Environment Variables
    const resendApiKey = env.RESEND_API_KEY;
    // Standard-Empfänger: beide E-Mail-Adressen
    const contactEmails = [
      'info@kost-sicherheitstechnik.de',
      'info@graphiks.de'
    ];

    if (!resendApiKey) {
      console.error('RESEND_API_KEY nicht gesetzt');
      return new Response(
        JSON.stringify({ error: 'Server-Konfiguration fehlt' }),
        {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // E-Mail über Resend senden
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
                </div>
                <div style="text-align: center; margin-top: 20px; color: #6e6e73; font-size: 12px;">
                  Diese E-Mail wurde über das Kontaktformular auf kost-sicherheitstechnik.de gesendet.
                </div>
              </div>
            </body>
          </html>
        `,
        text: `
Neue Anfrage über Website

Name: ${name}
Telefon: ${phone}
E-Mail: ${email}

Nachricht:
${message}

---
Diese E-Mail wurde über das Kontaktformular auf kost-sicherheitstechnik.de gesendet.
        `,
      }),
    });

    if (!emailResponse.ok) {
      const errorData = await emailResponse.text();
      console.error('Resend API Error:', emailResponse.status, errorData);
      // Detaillierte Fehlerinformationen für Debugging
      let errorMessage = 'E-Mail konnte nicht gesendet werden';
      try {
        const errorJson = JSON.parse(errorData);
        if (errorJson.message) {
          errorMessage = `Resend Fehler: ${errorJson.message}`;
        }
      } catch (e) {
        // Falls kein JSON, verwende Text
        errorMessage = `Resend Fehler: ${errorData}`;
      }
      return new Response(
        JSON.stringify({ error: errorMessage }),
        {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    const emailResult = await emailResponse.json();

    // Erfolgreiche Antwort
    return new Response(
      JSON.stringify({ 
        success: true, 
        message: 'Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns kurzfristig bei Ihnen.' 
      }),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );

  } catch (error) {
    console.error('Contact form error:', error);
    return new Response(
      JSON.stringify({ error: 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.' }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
}

// Helper: HTML-Escape für Sicherheit
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

