/**
 * API Endpoint zum Abrufen der gespeicherten Kontaktanfragen
 *
 * Geschützt mit API-Key (muss als Environment Variable gesetzt werden)
 *
 * Setup:
 * 1. Cloudflare Pages → Settings → Environment Variables
 * 2. Add: CONTACTS_API_KEY = (generiere einen sicheren Key)
 *
 * Nutzung:
 * GET /api/contacts?key=DEIN_API_KEY
 * GET /api/contacts?key=DEIN_API_KEY&date=2025-12-01  (für bestimmtes Datum)
 * GET /api/contacts?key=DEIN_API_KEY&id=contact_xxx  (einzelner Kontakt)
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json',
  };

  // API Key Validierung
  const apiKey = url.searchParams.get('key');
  const expectedKey = env.CONTACTS_API_KEY;

  if (!expectedKey) {
    return new Response(
      JSON.stringify({ error: 'API not configured' }),
      { status: 500, headers: corsHeaders }
    );
  }

  if (!apiKey || apiKey !== expectedKey) {
    return new Response(
      JSON.stringify({ error: 'Unauthorized' }),
      { status: 401, headers: corsHeaders }
    );
  }

  // KV Namespace
  const kv = env.CONTACT_BACKUP_KV || env.RATE_LIMIT_KV;

  if (!kv) {
    return new Response(
      JSON.stringify({ error: 'KV not configured' }),
      { status: 500, headers: corsHeaders }
    );
  }

  try {
    const contactId = url.searchParams.get('id');
    const date = url.searchParams.get('date');

    // Einzelnen Kontakt abrufen
    if (contactId) {
      const contact = await kv.get(contactId, { type: 'json' });
      if (!contact) {
        return new Response(
          JSON.stringify({ error: 'Contact not found' }),
          { status: 404, headers: corsHeaders }
        );
      }
      return new Response(
        JSON.stringify({ contact }),
        { status: 200, headers: corsHeaders }
      );
    }

    // Kontakte nach Datum abrufen
    if (date) {
      const indexKey = `index_${date}`;
      const contactIds = await kv.get(indexKey, { type: 'json' }) || [];

      const contacts = [];
      for (const id of contactIds) {
        const contact = await kv.get(id, { type: 'json' });
        if (contact) {
          contacts.push(contact);
        }
      }

      return new Response(
        JSON.stringify({
          date,
          count: contacts.length,
          contacts
        }),
        { status: 200, headers: corsHeaders }
      );
    }

    // Alle Kontakte der letzten 7 Tage auflisten
    const contacts = [];
    const today = new Date();

    for (let i = 0; i < 7; i++) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().slice(0, 10);
      const indexKey = `index_${dateStr}`;

      const contactIds = await kv.get(indexKey, { type: 'json' }) || [];

      for (const id of contactIds) {
        const contact = await kv.get(id, { type: 'json' });
        if (contact) {
          contacts.push(contact);
        }
      }
    }

    // Nach Datum sortieren (neueste zuerst)
    contacts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    return new Response(
      JSON.stringify({
        period: 'last_7_days',
        count: contacts.length,
        contacts
      }),
      { status: 200, headers: corsHeaders }
    );

  } catch (error) {
    console.error('Contacts API error:', error);
    return new Response(
      JSON.stringify({ error: 'Internal error' }),
      { status: 500, headers: corsHeaders }
    );
  }
}
