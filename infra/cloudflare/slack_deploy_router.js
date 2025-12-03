/**
 * Cloudflare Worker: Slack Deploy Router
 * 
 * Receives Slack slash commands (/deploy dev or /deploy prod)
 * and triggers GitHub Actions workflows via workflow_dispatch.
 */

// Slack signature verification
async function verifySlackSignature(request, body, signingSecret) {
  const timestamp = request.headers.get('X-Slack-Request-Timestamp');
  const signature = request.headers.get('X-Slack-Signature');
  
  if (!timestamp || !signature) {
    return false;
  }
  
  // Prevent replay attacks (5 minute window)
  const currentTime = Math.floor(Date.now() / 1000);
  if (Math.abs(currentTime - parseInt(timestamp)) > 300) {
    return false;
  }
  
  // Create signature base string
  const sigBaseString = `v0:${timestamp}:${body}`;
  
  // Create HMAC signature
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(signingSecret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  
  const signatureBytes = await crypto.subtle.sign(
    'HMAC',
    key,
    encoder.encode(sigBaseString)
  );
  
  const computedSignature = 'v0=' + Array.from(new Uint8Array(signatureBytes))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
  
  return computedSignature === signature;
}

// Parse Slack command
function parseSlackCommand(body) {
  const params = new URLSearchParams(body);
  const text = params.get('text') || '';
  const command = params.get('command');
  const user = params.get('user_name');
  
  // Parse /deploy dev or /deploy prod
  const env = text.trim().toLowerCase();
  if (env === 'dev' || env === 'development') {
    return { environment: 'dev', user };
  } else if (env === 'prod' || env === 'production') {
    return { environment: 'prod', user };
  }
  
  return null;
}

// Trigger GitHub Actions workflow
async function triggerGitHubWorkflow(env, githubToken, repoOwner, repoName) {
  const workflowFile = env === 'dev' ? 'deploy_dev.yml' : 'deploy_prod.yml';
  
  const url = `https://api.github.com/repos/${repoOwner}/${repoName}/actions/workflows/${workflowFile}/dispatches`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `token ${githubToken}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ref: 'main',
      inputs: {
        environment: env,
      },
    }),
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`GitHub API error: ${response.status} - ${errorText}`);
  }
  
  return response;
}

// Send Slack response
function sendSlackResponse(text, responseUrl) {
  return fetch(responseUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      response_type: 'in_channel',
    }),
  });
}

// Main handler
export default {
  async fetch(request, env) {
    // Only allow POST
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }
    
    try {
      // Get request body
      const body = await request.text();
      
      // Verify Slack signature
      const signingSecret = env.SLACK_SIGNING_SECRET;
      if (!signingSecret) {
        return new Response('SLACK_SIGNING_SECRET not configured', { status: 500 });
      }
      
      const isValid = await verifySlackSignature(request, body, signingSecret);
      if (!isValid) {
        return new Response('Invalid signature', { status: 401 });
      }
      
      // Parse command
      const parsed = parseSlackCommand(body);
      if (!parsed) {
        return new Response(JSON.stringify({
          text: '❌ Invalid command. Use `/deploy dev` or `/deploy prod`',
          response_type: 'ephemeral',
        }), {
          headers: { 'Content-Type': 'application/json' },
        });
      }
      
      const { environment, user } = parsed;
      
      // Get GitHub credentials
      const githubToken = env.GITHUB_TOKEN;
      const repoOwner = env.GITHUB_REPO_OWNER || 'carl'; // Default, should be set in env
      const repoName = env.GITHUB_REPO_NAME || 'ai-news-agent';
      
      if (!githubToken) {
        return new Response(JSON.stringify({
          text: '❌ GITHUB_TOKEN not configured',
          response_type: 'ephemeral',
        }), {
          headers: { 'Content-Type': 'application/json' },
        });
      }
      
      // Trigger GitHub Actions workflow
      await triggerGitHubWorkflow(environment, githubToken, repoOwner, repoName);
      
      // Get response URL for async response
      const params = new URLSearchParams(body);
      const responseUrl = params.get('response_url');
      
      // Determine URLs
      const domain = env.DOMAIN || 'ai-news-agent.pages.dev';
      const envUrl = environment === 'dev' 
        ? `https://dev.${domain}`
        : `https://${domain}`;
      
      const workflowUrl = `https://github.com/${repoOwner}/${repoName}/actions`;
      const workflowFile = environment === 'dev' ? 'deploy_dev.yml' : 'deploy_prod.yml';
      
      // Send immediate response
      const responseText = `🚀 Deploy started for ${environment.toUpperCase()} by @${user}\n\n` +
        `📦 Build logs: ${workflowUrl}\n` +
        `🌐 URL: ${envUrl}\n\n` +
        `⏳ Deployment in progress...`;
      
      // If response_url is available, send async response
      if (responseUrl) {
        sendSlackResponse(responseText, responseUrl).catch(console.error);
      }
      
      return new Response(JSON.stringify({
        text: responseText,
        response_type: 'in_channel',
      }), {
        headers: { 'Content-Type': 'application/json' },
      });
      
    } catch (error) {
      console.error('Error:', error);
      return new Response(JSON.stringify({
        text: `❌ Error: ${error.message}`,
        response_type: 'ephemeral',
      }), {
        headers: { 'Content-Type': 'application/json' },
        status: 500,
      });
    }
  },
};

