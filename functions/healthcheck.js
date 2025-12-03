/**
 * Cloudflare Pages Function: Health Check Endpoint
 * 
 * Returns health status for the application
 */

export async function onRequest(context) {
  const { request, env } = context;
  
  // Get git SHA from environment or default
  const version = env.GIT_SHA || "unknown";
  const environment = env.ENVIRONMENT || "unknown";
  
  const health = {
    status: "ok",
    time: new Date().toISOString(),
    version: version,
    environment: environment,
  };
  
  return new Response(JSON.stringify(health, null, 2), {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-cache",
    },
  });
}

