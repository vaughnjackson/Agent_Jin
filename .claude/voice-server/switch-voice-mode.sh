#!/bin/bash

# Switch between ElevenLabs and macOS native voice

VOICE_SERVER_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_PATH="$HOME/Library/LaunchAgents/com.pai.voice-server.plist"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "     PAI Voice Server - Mode Switcher"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Choose voice mode:"
echo "  1) ElevenLabs AI (requires API key, high quality)"
echo "  2) macOS Native (free, works offline)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    SERVER_FILE="server.ts"
    echo "✓ Switching to ElevenLabs AI voice"
elif [ "$choice" = "2" ]; then
    SERVER_FILE="server-macos.ts"
    echo "✓ Switching to macOS Native voice"
else
    echo "❌ Invalid choice"
    exit 1
fi

# Stop current server
echo "▶ Stopping current server..."
"$VOICE_SERVER_DIR/stop.sh" 2>/dev/null || true

# Update the LaunchAgent to use the selected server
if [ -f "$PLIST_PATH" ]; then
    # Backup current plist
    cp "$PLIST_PATH" "$PLIST_PATH.backup"

    # Update the server file in the plist
    sed -i '' "s|server.*\.ts|$SERVER_FILE|g" "$PLIST_PATH"

    echo "✓ Updated LaunchAgent configuration"
fi

# Start the server with new mode
echo "▶ Starting server..."
"$VOICE_SERVER_DIR/start.sh"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ Voice mode switched successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Test the new mode:"
echo "  curl -X POST http://localhost:8888/notify \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"message\": \"Testing voice mode\"}'"
