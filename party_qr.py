#!/usr/bin/env python3
"""
party_qr.py — Music Assistant Party Mode QR Code Generator
===========================================================
Connects to Music Assistant via WebSocket, fetches the party mode URL,
and generates a QR code PNG at /config/www/party_qr.png.

When party mode is inactive the PNG is deleted so the dashboard
falls back to the placeholder image automatically.

Usage:
    python3 party_qr.py

Requirements:
    pip install qrcode pillow websockets

Configuration:
    Set MA_WS to your Music Assistant WebSocket URL.
    Create /config/party_qr_token.txt containing your MA API token.

Getting your MA token:
    Music Assistant UI → Settings → Authentication → Create token
"""

import asyncio
import json
import os
import sys
import subprocess

# ── Configuration ────────────────────────────────────────────────────────────
MA_WS = "ws://YOUR_HA_IP:8095/ws"            # Music Assistant WebSocket URL (e.g. ws://192.168.1.100:8095/ws)
TOKEN_FILE = "/config/party_qr_token.txt"    # File containing MA API token
QR_PATH = "/config/www/party_qr.png"         # Output path (served as /local/party_qr.png)
# ─────────────────────────────────────────────────────────────────────────────


def ensure_deps():
    """Install required packages if not already present."""
    try:
        import qrcode
        import PIL
        import websockets
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "qrcode", "pillow", "websockets", "-q"
        ])


ensure_deps()

import qrcode
import websockets


async def main():
    # Read token
    try:
        with open(TOKEN_FILE, 'r') as f:
            token = f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: Token file not found: {TOKEN_FILE}")
        print("Create the file and paste your Music Assistant API token inside.")
        sys.exit(1)

    # Connect to Music Assistant
    async with websockets.connect(MA_WS) as ws:
        await ws.recv()  # server_info message

        # Authenticate
        await ws.send(json.dumps({
            "message_id": 1,
            "command": "auth",
            "args": {"token": token}
        }))
        auth_resp = json.loads(await ws.recv())

        if auth_resp.get("error_code"):
            print(f"ERROR: Auth failed: {auth_resp.get('details')}")
            sys.exit(1)

        print(f"Auth OK: {auth_resp['result']['user']['username']}")

        # Fetch party URL
        await ws.send(json.dumps({
            "message_id": 2,
            "command": "party/url"
        }))
        resp = json.loads(await ws.recv())
        url = resp.get("result")

    if url:
        print(f"Party mode active: {url}")
        _generate_qr(url)
    else:
        print("Party mode inactive")
        _remove_qr()


def _generate_qr(url: str) -> None:
    """Generate a white-on-transparent QR code PNG."""
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate black-on-white first (StyledPilImage works reliably this way)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        eye_drawer=RoundedModuleDrawer(),
    ).convert("RGBA")

    # Invert: black → white, white → transparent
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if (r + g + b) / 3 < 128:
                pixels[x, y] = (255, 255, 255, 255)   # dark → white
            else:
                pixels[x, y] = (0, 0, 0, 0)            # light → transparent

    img.save(QR_PATH)
    print(f"QR code saved: {QR_PATH}")


def _remove_qr() -> None:
    """Delete the QR PNG so the dashboard shows the placeholder."""
    if os.path.exists(QR_PATH):
        os.remove(QR_PATH)
        print(f"QR code deleted: {QR_PATH}")
    else:
        print("No QR file to delete.")


if __name__ == "__main__":
    asyncio.run(main())
