/**
 * Health Check Endpoint
 *
 * Prüft ob alle Services funktionieren:
 * - KV Backup verfügbar
 * - Resend API konfiguriert
 * - Turnstile konfiguriert
 *
 * GET /api/health
 * GET /api/health?key=API_KEY (für detaillierte Infos)
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json',
  };

  const apiKey = url.searchParams.get('key');
  const isAuthorized = apiKey && apiKey === env.CONTACTS_API_KEY;

  // Basic health check (public)
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '2.0.0',
    services: {
      email: !!env.RESEND_API_KEY,
      captcha: !!env.TURNSTILE_SECRET_KEY,
      backup: !!(env.CONTACT_BACKUP_KV || env.RATE_LIMIT_KV)
    }
  };

  // Alles muss funktionieren für "ok" Status
  const allServicesOk = health.services.email && health.services.backup;
  health.status = allServicesOk ? 'ok' : 'degraded';

  // Detaillierte Infos nur mit API Key
  if (isAuthorized) {
    const kv = env.CONTACT_BACKUP_KV || env.RATE_LIMIT_KV;

    // Zähle Kontakte der letzten 24h
    if (kv) {
      try {
        const today = new Date().toISOString().slice(0, 10);
        const todayIndex = await kv.get(`index_${today}`, { type: 'json' }) || [];
        health.stats = {
          contacts_today: todayIndex.length
        };
      } catch (e) {
        health.stats = { error: 'Could not fetch stats' };
      }
    }

    health.config = {
      email_configured: !!env.RESEND_API_KEY,
      turnstile_configured: !!env.TURNSTILE_SECRET_KEY,
      kv_backup_configured: !!env.CONTACT_BACKUP_KV,
      kv_ratelimit_configured: !!env.RATE_LIMIT_KV
    };
  }

  const statusCode = health.status === 'ok' ? 200 : 503;

  return new Response(
    JSON.stringify(health, null, 2),
    { status: statusCode, headers: corsHeaders }
  );
}
