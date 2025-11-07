/**
 * Cloudflare Pages Function für Kontaktformular
 * Sendet E-Mails über Resend API
 * 
 * Setup:
 * 1. Resend Account erstellen: https://resend.com
 * 2. API Key erstellen
 * 3. In Cloudflare Pages: Settings → Environment variables
 *    - RESEND_API_KEY: Dein Resend API Key
 * 
 * E-Mails werden an beide Adressen gesendet:
 *    - info@kost-sicherheitstechnik.de
 *    - info@graphiks.de
 */

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
    // Formular-Daten parsen
    const formData = await request.formData();
    const name = formData.get('name');
    const phone = formData.get('phone');
    const email = formData.get('email');
    const message = formData.get('message');

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

