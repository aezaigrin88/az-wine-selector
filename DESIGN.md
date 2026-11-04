---
name: Wine & Terroir Atlas
description: Личный винный и терруарный атлас в картографической эстетике chartbook_geoeconomics (Vintage Atlas)
colors:
  crimson-archival: "#8A0D2F"
  prussian-deep: "#2C4F6B"
  prussian-faded: "#3B6E8F"
  verdigris-oxidised: "#4A6B52"
  amber-burnt: "#C85A17"
  brass-patina: "#B8963E"
  paper-vellum: "#F5F2E6"
  paper-card: "#FDF5E6"
  paper-warm: "#EFEAD8"
  map-land: "#F3EDE0"
  map-relief: "#E3D9C6"
  map-slope: "#D8CCB4"
  map-forest: "#DCE0D3"
  map-water: "#A8BCC9"
  ink-primary: "#2F2926"
  ink-secondary: "#484E4F"
  foxing-border: "#C4B69A"
typography:
  display:
    fontFamily: "'SB Sans Interface', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "1.25rem"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "'SB Sans Interface', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "1.08rem"
    fontWeight: 700
    lineHeight: 1.28
  title:
    fontFamily: "'SB Sans Interface', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "0.92rem"
    fontWeight: 700
    lineHeight: 1.35
    letterSpacing: "0.03em"
  body:
    fontFamily: "'SB Sans Interface', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "'SB Sans Interface', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "0.80rem"
    fontWeight: 600
    lineHeight: 1.35
rounded:
  sm: "4px"
  md: "8px"
spacing:
  xs: "6px"
  sm: "10px"
  md: "16px"
  lg: "26px"
components:
  button-primary:
    backgroundColor: "{colors.crimson-archival}"
    textColor: "{colors.paper-card}"
    rounded: "{rounded.sm}"
    padding: "8px 14px"
  button-secondary:
    backgroundColor: "{colors.paper-card}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "8px 14px"
  pill-filter:
    backgroundColor: "{colors.paper-card}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "6px 11px"
  pill-filter-active:
    backgroundColor: "{colors.prussian-deep}"
    textColor: "{colors.paper-card}"
    rounded: "{rounded.sm}"
    padding: "6px 11px"
  atlas-card:
    backgroundColor: "{colors.paper-card}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.md}"
    padding: "16px"
---

# Design System: Wine & Terroir Atlas

## Overview

**Creative North Star: "The Cartographer's Cellar Ledger (`chartbook_geoeconomics`)"**

The Wine & Terroir Atlas treats a personal wine tasting collection as a living cartographic publication modeled directly on the `chartbook_geoeconomics` Vintage Atlas system. Rather than presenting tasted bottles as dark-mode SaaS cards or generic rating tiles, the interface pairs a multi-scale parchment map plate (switching between European/Crimean vineyard parcels and Moscow tasting venues) with a structured archival terroir passport and ledger table.

Every surface evokes engraved survey plates printed on warm cotton vellum: `2px` charcoal-sepia frames, overprinted ink header banners, faded Prussian slate-blue river networks, limestone escarpment contours, L-shaped metric scale bars, and haloed `SB Sans Interface` typography.

**Key Characteristics:**
- Dual-layer interactive cartographic plate (1. Терруары и парцели vs 2. Места дегустаций в Москве) plus 300 DPI static publication plates.
- Warm archival paper hierarchy (`#F5F2E6` canvas, `#FDF5E6` card stock, `#EFEAD8` toolbar strips) paired with deep charcoal-sepia ink (`#2F2926`).
- Wine-style semantic coding grounded in archival ink pigments: Archival Crimson (`#8A0D2F`) for red wines, Faded Prussian Blue (`#3B6E8F`) for white wines, and Burnt Amber (`#C85A17`) for sparkling wines.
- Self-hosted `SB Sans Interface` across UI controls, cartographic labels, and tabular numeric columns (`tabular-nums`).

## Colors

The palette combines archival vellum neutrals with mineral cartographic pigments drawn directly from `chartbook_geoeconomics`.

### Primary
- **Archival Crimson** (`#8A0D2F`): Primary action buttons, red wine parcel pins, active map-mode tabs, and the terroir passport header band.
- **Deep Map-Plate Blue** (`#2C4F6B`): Cartographic plate header band, active region pills, and external Vivino links.

### Secondary
- **Faded Prussian Blue** (`#3B6E8F`): White wine parcel markers (Chardonnay, Aligoté, Pinot Blanc) and river/water typography.
- **Burnt Amber** (`#C85A17`): Sparkling wine markers (Champagne Grand Cru, Crémant de Bourgogne, Corpinnat) and star rating highlights.

### Tertiary
- **Oxidised Verdigris** (`#4A6B52`): Save confirmation indicators and tasting session accents.
- **Patina Brass** (`#B8963E`): Keyboard `:focus-visible` rings, active marker halos, and selection highlights.

### Neutral
- **Vellum Field** (`#F5F2E6`): Root page background.
- **Light Parchment Card** (`#FDF5E6`): Primary surface for the map plate, terroir dossier, and ledger table.
- **Warm Toolbar Strip** (`#EFEAD8`): Secondary neutral layer for filter bars, map toolbars, and footers.
- **Map Cartographic Fills** (`#F3EDE0` land, `#E3D9C6` escarpment relief, `#D8CCB4` sub-appellation slope, `#DCE0D3` forest/park, `#A8BCC9` water body with `#7C98AB` shoreline).
- **Charcoal-Sepia Ink** (`#2F2926`): Primary text, table headers, and `2px` structural borders.
- **Slate-Umber Secondary Ink** (`#484E4F`): Subtitles, metadata captions, and secondary specifications (`>= 7:1` contrast on parchment).

### Named Rules
**The Pigment-Means-Style Rule.** Archival Crimson (`#8A0D2F`), Faded Prussian Blue (`#3B6E8F`), and Burnt Amber (`#C85A17`) encode wine styles (Red, White, Sparkling) across map pins, legend swatches, and table badges. Never repurpose these three pigments for unrelated decorative chrome.

**The Haloed Cartographic Label Rule.** Every text label placed over the map canvas must carry a `3px` `#FDF5E6` stroke halo (`paint-order: stroke`) so commune and parcel names remain legible across rivers, roads, and appellation boundaries.

## Typography

**Display & UI Font:** `'SB Sans Interface'` (self-hosted `.ttf` in `fonts/`, weights 400, 600, 700, plus italic)

**Character:** A crisp, high-legibility humanist grotesque that bridges dense statistical tables, Russian/French cartographic nomenclature (*lieux-dits*, communes, appellations), and compact UI controls without ornamental distraction.

### Hierarchy
- **Display** (`700`, `1.25rem`, `1.25` line-height, `-0.01em` tracking): Application title in the sticky top bar.
- **Headline** (`700`, `1.08rem`, `1.28` line-height): Selected bottle title in the dossier and top-level section headings.
- **Title** (`700`, `0.92rem`, `1.35` line-height, `0.03em` tracking, uppercase): Overprinted `.qcard-header` bands on primary plates.
- **Body** (`400` / `500`, `0.9375rem`, `1.5` line-height): Tasting notes, soil descriptions, and ledger cells.
- **Label** (`600`, `0.80rem`, `1.35` line-height): Filter pills, region presets, specification keys, and scale-bar readouts.

### Named Rules
**The Tabular Vintage & Coordinate Rule.** All vintages (`2018`, `2022`), alcohol percentages (`13.0%`), ratings (`4.5 / 5.0`), coordinates (`46.993° N`), and Vivino IDs must apply `font-variant-numeric: tabular-nums`.

**The Self-Standing Heading Rule.** Headings never carry an uppercase kicker, eyebrow, or decorative `01 / 02` number above them; `.qcard-header` bands and `<h2>` headings carry their own hierarchy directly.

## Layout

The interface uses a `1480px` maximum container (`20px` horizontal padding on desktop, `12px` on mobile) structured around an immediate operational first viewport:
- **Sticky Top Atlas Bar**: Brand title, live collection counter (`17 бутылок · 9 красных · 4 белых · 4 игристых`), primary `+ Записать бутылку` drawer trigger, and 1-click JSON export.
- **First-Viewport Split Workspace (`grid-template-columns: minmax(0, 1.85fr) minmax(340px, 1fr)`, `18px` gap)**:
  - Left `2/3`: Interactive Cartographic Plate (`540px` height on desktop, `400px` on mobile) with layer tabs, regional zoom presets, vector SVG map / 300 DPI static plate viewer, flat legend ribbon, and source caption bar.
  - Right `1/3`: Active Bottle & Terroir Dossier displaying the bottle label photograph, front/back photo toggle, interactive 5-star rating widget, 6-row terroir passport table, live-saved tasting notes, and direct Vivino link.
- **Archival Ledger & Session Timeline**: Full-width searchable, filterable table of all 17 bottles followed by a responsive grid (`repeat(auto-fill, minmax(310px, 1fr))`) of tasting session cards.

## Elevation & Depth

Surfaces combine crisp `2px solid #2F2926` ink framing with a soft directional plate shadow and tonal parchment layering (`#F5F2E6` page -> `#FDF5E6` card -> `#EFEAD8` toolbar strip).

### Shadow Vocabulary
- **Atlas Plate Shadow** (`box-shadow: 0 6px 18px rgba(47, 41, 38, 0.10), 0 2px 6px rgba(59, 110, 143, 0.12)`): Applied to top-level `.atlas-card` and `.session-card` containers.
- **Control Hover Lift** (`box-shadow: 0 3px 8px rgba(47, 41, 38, 0.12)` with `translateY(-1px)`): Applied to `.btn` controls on hover.

### Named Rules
**The No-Nested-Card Rule.** Inside a bordered `.atlas-card`, child sections (map toolbars, legend ribbons, rating rows, specification tables, and note editors) must separate via `1px` horizontal rules (`#C4B69A` / `#DFD5C0`) and tonal background strips rather than nesting a bordered card inside a bordered card.

## Shapes

- **Primary Plates & Cards**: `8px` border radius (`--radius-md`) with `2px solid #2F2926` structural borders and full-bleed top header bands (`.qcard-header`).
- **Buttons, Inputs & Filter Pills**: `4px` border radius (`--radius-sm`) with `1px`–`1.5px` borders.
- **Cartographic Markers**: Distinct geometric silhouettes by wine style — circles for Red wines, rounded squares for White wines, and rotated diamonds for Sparkling wines — each framed by a `2px` `#FDF5E6` stroke.

## Components

### Buttons (`.btn`, `.btn-primary`)
- **Shape:** Gently rounded corners (`4px` radius) with `1.5px solid #2F2926` border and `8px 14px` padding.
- **Primary:** Archival Crimson (`#8A0D2F`) fill with `#FDF5E6` text; darkens to `#6E0924` on hover with `-1px` vertical lift.
- **Secondary:** Light Parchment (`#FDF5E6`) fill with `#2F2926` text; shifts to `#EFEAD8` on hover.

### Filter & Region Pills (`.pill-btn`)
- **Style:** Compact (`6px 11px` padding, `4px` radius, `0.80rem` weight `600`) with `1px solid #7A7267` border on `#FDF5E6`.
- **State:** Active region/filter state fills with Deep Map-Plate Blue (`#2C4F6B`) or Archival Crimson (`#8A0D2F`) and `#FDF5E6` text.

### Cards / Containers (`.atlas-card`, `.session-card`)
- **Corner Style:** `8px` radius.
- **Background:** `#FDF5E6` with `#EFEAD8` utility bars.
- **Border:** `2px solid #2F2926` with top `.qcard-header` banner.
- **Internal Padding:** `16px` body padding (`11px 16px` on header bars).

### Inputs / Fields (`.form-input`, `.search-input`, `.notes-textarea`)
- **Style:** `1.5px solid #8A8175` border on warm white `#FFFDF7`, `4px` radius, `8px 11px` padding.
- **Focus:** Border shifts to `#2C4F6B` with a `2px solid #B8963E` focus-visible ring.

### Interactive Cartographic Plate (`#atlasSvgMap`)
- **Behavior:** Supports drag-pan, `+`/`−`/reset zoom controls, 1-click regional bounding-box presets, layer switching between European/Crimean terroir parcels and Moscow tasting venues, and coordinate picking when logging a new bottle.

## Do's and Don'ts

### Do:
- **Do** use the exact `chartbook_geoeconomics` cartographic palette (`#F3EDE0` land, `#E3D9C6` slope relief, `#DCE0D3` forest, `#A8BCC9` water, `#7C98AB` shoreline) on all interactive and static map plates.
- **Do** pair every wine entry with its parcel-level geography (*commune*, *lieu-dit*, coordinates, and soil profile) alongside its Moscow tasting session date and venue.
- **Do** keep credentials (`VIVINO_EMAIL`, `VIVINO_PASSWORD`) strictly outside the repository in `C:\Users\timza\.env` when running `sync_vivino.py`.

### Don't:
- **Don't** nest bordered cards inside `.atlas-card` containers; use horizontal hairline dividers (`#DFD5C0`) and tonal bands (`#EFEAD8`) instead.
- **Don't** place uppercase kickers/eyebrows or `01 / 02` section numbers above headings.
- **Don't** substitute Unicode geometric symbols (`●`, `■`, `◆`, `★`) for inline SVG icons or matplotlib scatter markers.
