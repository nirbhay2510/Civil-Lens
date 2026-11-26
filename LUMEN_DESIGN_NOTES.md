# Lumen — CivilLens interface notes

Lumen is the visual system behind the CivilLens research console (`web/`).

## Layout
- A single **top rail** carries the brand mark, the eleven stations (Summary, Scan Studio, Corpus Vault, Prep Bench, Engine Garage, Insight Room, Payoff Tuning, Equity Audit, Trials, Briefs & Manuscript, Preferences), the skin switch and the revision tag.
- A thin status strip under the rail shows the active engine and the formal problem statement.
- Content sits in a centred stage (max 1320 px). Cards are "tiles" with a teal top edge and an offset, hard-edged shadow.

## Colour
| Role | Light | Night |
|------|-------|-------|
| Ground | `#F3F6F8` | `#0B141A` |
| Slab (cards) | `#FFFFFF` | `#121E26` |
| Graphite (text) | `#0B2530` | `#E8F1F5` |
| Lead (brand tint) | `#0E7C86` | `#3CC9D3` |
| Beacon (alerts) | `#D9363E` | `#FF6B72` |
| Sage (good) | `#2F9E44` | `#4CD08A` |
| Heed (warning) | `#C77700` | `#C77700` |

## Type
No web fonts are shipped. Headlines use a Palatino/Georgia serif stack, body copy a humanist system sans, data a system monospace.

## Shape
Corners are 2–8 px, chips are rectangular tags, buttons are uppercase with wide tracking, and hover lifts a tile by 2 px while its shadow turns teal.

## Files
- `web/home.html` — markup
- `web/styles/lumen.css` — tokens, layout and components
- `web/scripts/gateway.js` — REST client for `/api/*`
- `web/scripts/console.js` — page controller
