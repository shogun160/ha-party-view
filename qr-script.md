# QR Code Script Setup

The script `scripts/party_qr.py` generates a QR code linking to the  
Music Assistant party mode URL. When party mode is off the PNG is deleted  
and the dashboard falls back to a placeholder image.

---

## 1. Copy the script

```bash
cp scripts/party_qr.py /config/python_scripts/party_qr.py
```

> **Note:** Home Assistant's built-in `python_script` integration does **not** support  
> async code or third-party packages. Run this script via `shell_command` instead.

---

## 2. Create the token file

Open Music Assistant → **Settings** → **Authentication** → **Create token**.  
Copy the token and save it:

```bash
echo "YOUR_TOKEN_HERE" > /config/party_qr_token.txt
chmod 600 /config/party_qr_token.txt
```

---

## 3. Add a shell_command to HA

Add the following to your `configuration.yaml`:

```yaml
shell_command:
  party_qr: "python3 /config/python_scripts/party_qr.py"
```

Reload Home Assistant configuration after saving.

---

## 4. Test manually

Run the script from the HA terminal (SSH or terminal add-on):

```bash
python3 /config/python_scripts/party_qr.py
```

Expected output when party mode is **active**:
```
Auth OK: admin
Party mode active: http://YOUR_HA_IP:8095/#/party
QR code saved: /config/www/party_qr.png
```

Expected output when party mode is **inactive**:
```
Auth OK: admin
Party mode inactive
No QR file to delete.
```

---

## 5. Verify the image is served

Open in your browser:
```
http://homeassistant.local:8123/local/party_qr.png
```

You should see a white-on-transparent QR code.

---

## Placeholder image

When `party_qr.png` does not exist, the dashboard displays  
`/local/spotify_device_pics/player_off.png` at 50% opacity.

Replace this with any image you prefer by changing the path in  
`party-view.yaml` (search for `player_off.png`).

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Token file not found` | Create `/config/party_qr_token.txt` |
| `Auth failed` | Check token is correct and not expired |
| `Connection refused` | Verify `MA_WS` URL and port (default: 8095) |
| QR image not visible | Check `/config/www/` is writable |
| Packages not installed | Run `pip install qrcode pillow websockets` |
