/**
 * Middleware für alle Requests
 * - Redirected non-www auf www (301)
 * - Gilt für alle Seiten
 */

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);

  // Redirect non-www to www (301 Permanent Redirect)
  if (url.hostname === 'kost-sicherheitstechnik.de') {
    const newUrl = new URL(request.url);
    newUrl.hostname = 'www.kost-sicherheitstechnik.de';
    return Response.redirect(newUrl.toString(), 301);
  }

  // Continue with normal request
  return next();
}
