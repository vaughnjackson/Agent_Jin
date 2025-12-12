# macOS Native Voice Guide

## Overview

Your voice server can run in **two modes**:

| Mode | Cost | Quality | Offline | API Key Required |
|------|------|---------|---------|------------------|
| **ElevenLabs** | $0-11/mo* | High (AI voices) | ❌ No | ✅ Yes |
| **macOS Native** | FREE | Good (built-in) | ✅ Yes | ❌ No |

*ElevenLabs has 10,000 chars/month free tier

## Switch Between Modes

### Quick Switch

```bash
cd ~/.claude/voice-server
./switch-voice-mode.sh
```

Follow the prompts to choose:
- **Option 1:** ElevenLabs AI (high quality, requires API key)
- **Option 2:** macOS Native (free, works offline)

### Manual Switch

**To macOS Native:**
```bash
cd ~/.claude/voice-server
./stop.sh
# Edit LaunchAgent to use server-macos.ts instead of server.ts
./start.sh
```

**To ElevenLabs:**
```bash
cd ~/.claude/voice-server
./stop.sh
# Edit LaunchAgent to use server.ts
./start.sh
```

## macOS Voice Options

### Available Voices

List all available macOS voices:
```bash
say -v '?'
```

### Popular English Voices

| Voice | Gender | Region | Description |
|-------|--------|--------|-------------|
| **Samantha** | Female | US | Default, clear and natural |
| **Alex** | Male | US | Classic macOS voice |
| **Daniel** | Male | UK | British accent |
| **Karen** | Female | AU | Australian accent |
| **Fiona** | Female | UK | Scottish accent |
| **Fred** | Male | US | Older gentleman |
| **Victoria** | Female | US | Professional |
| **Allison** | Female | US | Friendly |
| **Tom** | Male | US | Deep voice |
| **Serena** | Female | UK | Elegant British |

### Test a Voice

```bash
say -v Samantha "Hello! I am Samantha, the default macOS voice."
say -v Alex "I'm Alex, a classic Mac voice."
say -v Daniel "I'm Daniel, speaking with a British accent."
```

### Set Default Voice for PAI

Add to `~/.env`:
```bash
MACOS_VOICE=Samantha
```

Or choose a different voice:
```bash
echo "MACOS_VOICE=Alex" >> ~/.env
```

## Using macOS Native Voice

### Send Notification with Default Voice

```bash
curl -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from macOS native voice!"}'
```

### Send Notification with Specific Voice

```bash
curl -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Testing different voices",
    "voice": "Daniel"
  }'
```

### Disable Voice (Visual Notification Only)

```bash
curl -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Silent notification",
    "voice_enabled": false
  }'
```

## Comparison: ElevenLabs vs macOS Native

### ElevenLabs Advantages
- ✅ Ultra-realistic AI voices
- ✅ Multiple premium voice options
- ✅ Emotional tone control
- ✅ Multi-language support (better)
- ✅ Professional quality

### macOS Native Advantages
- ✅ **Completely free**
- ✅ **Works offline**
- ✅ **No API key needed**
- ✅ **Zero setup**
- ✅ **No rate limits**
- ✅ **Privacy - nothing sent to cloud**
- ✅ Instant response (no network delay)
- ✅ Built into macOS (always available)

## Recommendation

**Use macOS Native if:**
- You want zero cost
- You need offline capability
- You don't have ElevenLabs API key
- Privacy is a priority (no data sent externally)
- You're testing/developing

**Use ElevenLabs if:**
- You want the highest quality AI voices
- You're doing demos/presentations
- You have API credits to use
- You want specific voice personalities

## Download Additional Voices

macOS allows downloading more voices:

1. **System Settings** → **Accessibility** → **Spoken Content**
2. Click **System Voice** dropdown
3. Click **Customize...**
4. Download additional voices (many are free!)

Premium voices available include:
- Siri voices (very natural)
- Enhanced voices (higher quality)
- Multiple languages

## Current Configuration

Check your current voice mode:
```bash
curl http://localhost:8888/health
```

Look for `"voice_system"` in the response:
- `"ElevenLabs"` = Using AI voices
- `"macOS Native (say)"` = Using built-in voices

## Troubleshooting

### "Voice not found"
The voice name is case-sensitive. Check available voices:
```bash
say -v '?' | grep -i "voice_name"
```

### "No sound"
Check macOS volume and sound output settings.

### "Server not responding"
Restart the voice server:
```bash
cd ~/.claude/voice-server
./restart.sh
```

---

**💡 Tip:** Start with macOS Native (free) and switch to ElevenLabs later if you want higher quality!
