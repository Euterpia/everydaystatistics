/**
 * Cloudflare Pages Function: POST /api/subscribe
 *
 * Accepts a form submission with `email` (required) and `name` (optional),
 * adds the subscriber to the MailerLite "44-Day Statistics Course" group,
 * and redirects to /subscribed on success.
 *
 * Environment variable required (set in Cloudflare Pages dashboard):
 *   MAILERLITE_API_KEY — the MailerLite API token
 */

const MAILERLITE_GROUP_ID = "185022876953347433";
const MAILERLITE_API      = "https://connect.mailerlite.com/api";

export async function onRequestPost(context) {
  const { request, env } = context;
  const apiKey = env.MAILERLITE_API_KEY;

  if (!apiKey) {
    return new Response("Server configuration error", { status: 500 });
  }

  // Parse form body
  let email, name;
  const contentType = request.headers.get("content-type") || "";
  if (contentType.includes("application/x-www-form-urlencoded")) {
    const text = await request.text();
    const params = new URLSearchParams(text);
    email = (params.get("email") || "").trim().toLowerCase();
    name  = (params.get("name")  || "").trim();
  } else if (contentType.includes("application/json")) {
    const body = await request.json();
    email = (body.email || "").trim().toLowerCase();
    name  = (body.name  || "").trim();
  } else {
    return new Response("Unsupported content type", { status: 415 });
  }

  // Basic validation
  if (!email || !email.includes("@")) {
    return Response.redirect(new URL("/subscribed?error=invalid", request.url).href, 303);
  }

  // Build subscriber payload
  const payload = {
    email,
    groups: [MAILERLITE_GROUP_ID],
    status: "active",
  };
  if (name) payload.fields = { name };

  // Call MailerLite
  try {
    const mlRes = await fetch(`${MAILERLITE_API}/subscribers`, {
      method:  "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type":  "application/json",
        "Accept":        "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!mlRes.ok) {
      const err = await mlRes.text();
      console.error("MailerLite error:", mlRes.status, err);
      // Subscriber already exists (409) is fine — they just re-signed up
      if (mlRes.status !== 409 && mlRes.status !== 422) {
        return Response.redirect(new URL("/subscribed?error=ml", request.url).href, 303);
      }
    }
  } catch (e) {
    console.error("Fetch error:", e);
    return Response.redirect(new URL("/subscribed?error=network", request.url).href, 303);
  }

  return Response.redirect(new URL("/subscribed", request.url).href, 303);
}

// Return 405 for non-POST requests
export async function onRequest(context) {
  return new Response("Method not allowed", { status: 405 });
}
