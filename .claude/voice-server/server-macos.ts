#!/usr/bin/env bun
/**
 * PAI Voice Server - macOS Native Version
 * Uses macOS built-in 'say' command instead of ElevenLabs
 * 100% free, works offline, no API key needed
 */

import { serve } from "bun";
import { spawn } from "child_process";

const PORT = parseInt(process.env.PORT || "8888");
const DEFAULT_VOICE = process.env.MACOS_VOICE || "Samantha"; // Default macOS voice

// Sanitize input for shell commands
function sanitizeForShell(input: string): string {
  return input.replace(/[^a-zA-Z0-9\s.,!?\-']/g, '').trim().substring(0, 500);
}

// Validate input
function validateInput(input: any): { valid: boolean; error?: string } {
  if (!input || typeof input !== 'string') {
    return { valid: false, error: 'Invalid input type' };
  }
  if (input.length > 500) {
    return { valid: false, error: 'Message too long (max 500 characters)' };
  }
  return { valid: true };
}

// Spawn safe child process
function spawnSafe(command: string, args: string[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      stdio: 'ignore',
      detached: false,
    });
    child.on('error', reject);
    child.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`Process exited with code ${code}`));
    });
  });
}

// Speak using macOS say command
async function speakText(text: string, voice: string = DEFAULT_VOICE) {
  const safeText = sanitizeForShell(text);
  try {
    console.log(`🎙️  Speaking with macOS voice: ${voice}`);
    await spawnSafe('/usr/bin/say', ['-v', voice, safeText]);
  } catch (error) {
    console.error("Failed to speak:", error);
  }
}

// Send macOS notification
async function sendNotification(
  title: string,
  message: string,
  voiceEnabled = true,
  voice: string = DEFAULT_VOICE
) {
  const titleValidation = validateInput(title);
  const messageValidation = validateInput(message);

  if (!titleValidation.valid) throw new Error(`Invalid title: ${titleValidation.error}`);
  if (!messageValidation.valid) throw new Error(`Invalid message: ${messageValidation.error}`);

  const safeTitle = sanitizeForShell(title);
  const safeMessage = sanitizeForShell(message);

  // Speak the message using macOS say
  if (voiceEnabled) {
    await speakText(safeMessage, voice);
  }

  // Display macOS notification
  try {
    const script = `display notification "${safeMessage}" with title "${safeTitle}" sound name ""`;
    await spawnSafe('/usr/bin/osascript', ['-e', script]);
  } catch (error) {
    console.error("Notification display error:", error);
  }
}

// Rate limiting
const requestCounts = new Map<string, { count: number; resetTime: number }>();
const RATE_LIMIT = 10;
const RATE_WINDOW = 60000;

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const record = requestCounts.get(ip);

  if (!record || now > record.resetTime) {
    requestCounts.set(ip, { count: 1, resetTime: now + RATE_WINDOW });
    return true;
  }

  if (record.count >= RATE_LIMIT) return false;

  record.count++;
  return true;
}

// Start HTTP server
const server = serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url);
    const clientIp = req.headers.get('x-forwarded-for') || 'localhost';

    const corsHeaders = {
      'Access-Control-Allow-Origin': 'http://localhost:*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (req.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Only allow localhost
    if (!clientIp.includes('localhost') && !clientIp.includes('127.0.0.1')) {
      return new Response('Forbidden', { status: 403 });
    }

    // Rate limiting
    if (!checkRateLimit(clientIp)) {
      return new Response('Rate limit exceeded', { status: 429 });
    }

    // Health check endpoint
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'healthy',
        port: PORT,
        voice_system: 'macOS Native (say)',
        default_voice: DEFAULT_VOICE,
        api_key_required: false
      }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders }
      });
    }

    // Notification endpoint
    if (url.pathname === '/notify' && req.method === 'POST') {
      try {
        const body = await req.json();
        const title = body.title || 'PAI Notification';
        const message = body.message;
        const voiceEnabled = body.voice_enabled !== false;
        const voice = body.voice || DEFAULT_VOICE;

        if (!message) {
          return new Response(JSON.stringify({ status: 'error', message: 'Message required' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });
        }

        console.log(`📨 Notification: "${title}" - "${message}" (voice: ${voiceEnabled}, macOS voice: ${voice})`);

        await sendNotification(title, message, voiceEnabled, voice);

        return new Response(JSON.stringify({ status: 'success', message: 'Notification sent' }), {
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      } catch (error: any) {
        console.error('Error:', error);
        return new Response(JSON.stringify({ status: 'error', message: error.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      }
    }

    return new Response('Not Found', { status: 404 });
  },
});

console.log(`
🎙️  PAI Voice Server (macOS Native) started
📍 Port: ${PORT}
🗣️  Voice System: macOS 'say' command
🎵 Default Voice: ${DEFAULT_VOICE}
🔒 Security: CORS restricted to localhost, rate limiting enabled
💰 Cost: FREE - no API key needed!
🌐 Health: http://localhost:${PORT}/health
`);
