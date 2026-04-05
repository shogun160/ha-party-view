# Automation Setup

The automation in `automation/party_mode.yaml` calls the QR script  
whenever the Music Assistant player state changes — this covers  
party mode starting and stopping.

---

## Prerequisites

Complete the [QR Script Setup](qr-script.md) first so the  
`shell_command.party_qr` service exists.

---

## Option A — Paste into automations.yaml

Copy the content of `automation/party_mode.yaml` into your  
`/config/automations.yaml` and reload automations:

```bash
# In HA Developer Tools → Services:
service: automation.reload
```

---

## Option B — Import via HA UI

1. Go to **Settings → Automations & Scenes**
2. Click **+ Create automation** → **Create new automation**
3. Switch to YAML mode (three dots top right)
4. Paste the content of `automation/party_mode.yaml`
5. Save

---

## How it works

```
Music Assistant player state changes
        ↓
HA automation triggers
        ↓
shell_command.party_qr runs python3 /config/python_scripts/party_qr.py
        ↓
Script connects to MA WebSocket
        ↓
Party mode active?  → Generate QR PNG → Dashboard shows QR code
Party mode inactive → Delete QR PNG   → Dashboard shows placeholder
```

---

## Manual trigger

You can also call the script manually from **Developer Tools → Services**:

```yaml
service: shell_command.party_qr
```

Or trigger the automation directly:

```yaml
service: automation.trigger
target:
  entity_id: automation.party_mode_qr_code_aktualisieren
```

---

## Tablet auto-navigation (optional)

To automatically open the Party View on your tablet when party mode starts,  
add a second action to the automation using Fully Kiosk Browser:

```yaml
action:
  - service: shell_command.party_qr
  - choose:
      - conditions:
          - condition: template
            value_template: >
              {{ state_attr('media_player.kuche_2', 'active_queue') is not none }}
        sequence:
          - service: fully_kiosk.load_url
            data:
              device_id: YOUR_FULLY_KIOSK_DEVICE_ID
              url: http://YOUR_HA_IP:8123/YOUR_PARTY_VIEW
```

Find your Fully Kiosk `device_id` in **Settings → Devices & Services → Fully Kiosk**.
