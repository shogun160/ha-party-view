# Customisation

## Layout dimensions

All layout values are in `party-view.yaml` under `layout:`:

```yaml
layout:
  grid-template-columns: 37% 63%      # left/right column ratio
  grid-template-rows: 465px 100px 60px # queue / controls / volume height
  height: calc(100vh - 180px)          # total grid height (100vh - top - bottom padding)
  padding: 90px 90px 90px 50px         # top right bottom left
  gap: 16px                            # gap between grid cells
```

### Adjusting the queue height

Increase `465px` to show more tracks, decrease to push controls higher.  
`height` must match: `100vh - (top padding) - (bottom padding)`.

---

## Background blur

Controlled by the first `button-card` in the stack:

```yaml
- filter: blur(40px) brightness(0.5)
- transform: scale(1.15)
```

- Increase `blur` for more blur
- Decrease `brightness` (e.g. `0.3`) for a darker background
- Increase `scale` to avoid edge artifacts with high blur values

---

## Queue mask gradient

The queue fades out at the top and bottom via CSS mask:

```js
'mask-image:linear-gradient(to bottom, transparent 0%, black 12%, black 100%, transparent 100%)'
```

- `12%` — how far down before the queue becomes fully visible
- `100%` — change the second `100%` to e.g. `90%` to add a fade-out at the bottom

---

## Player button sizing

In the `controls` card's `custom_fields`:

| Button | Size |
|--------|------|
| prev / next / fav | 44 × 44 px |
| play / pause | 56 × 56 px |

Adjust `width` and `height` in the respective `styles.card` section.

---

## Column ratio

The left column (QR + floorplan) vs right column (queue + controls):

```yaml
grid-template-columns: 37% 63%
```

Change to e.g. `30% 70%` for a narrower left column.

---

## Favourite button

The `fav` custom field calls `button.press` on a Music Assistant  
"Favourite current track" button entity. If you don't have this,  
replace it with any other action or remove the field and adjust  
`grid-template-areas` and `grid-template-columns` accordingly.

---

## Floorplan image

Replace `/local/floorplan/00_Aus_Alles.png` with any image  
served from `/config/www/`. Paste the `/local/...` path into the  
floorplan `button-card` label.

---

## QR placeholder image

When party mode is off the dashboard shows a placeholder at 50% opacity.  
Change the path in the QR `button-card` label:

```js
const placeholder = '/local/your-custom-placeholder.png';
```
