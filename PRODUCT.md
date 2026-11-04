# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: Responsive static HTML/CSS/JS PWA (works seamlessly on desktop and mobile phones, zero build step, deployable to GitHub Pages or opened locally, backed by a structured JSON catalog and optional local Python sync script for Vivino).

## Users

Primary user: Artem Zaigrin (`@artem_zaigrin`, Vivino `user_id: 77968357`, `cellar_id: 6491870`), recording and exploring wines tasted at home, tastings (`burgundy.ru`), and restaurants from both desktop and mobile phone.

## Product Purpose

A personal wine cellar atlas and tasting journal that maps every tasted bottle to:
1. Its exact **terroir of origin** — country, region, sub-region/village, and specific *climat* / *lieu-dit* parcel (e.g. `En Cuillery` in Monthélie, `Les Argillats` in Nuits-Saint-Georges, `Les Autrots` in Bourgogne, `En Buzigny` in Meursault/Coteaux Bourguignons, `Chasne` in Hautes-Côtes, `La Folie` in Brouilly, Avize Grand Cru in Champagne, Subirats/Penedès for Corpinnat, Verkhnesadovoe in Sevastopol).
2. The **place and occasion of tasting** — tasting venue (`burgundy.ru`, home, restaurant), date, companions/context, star rating, tasting notes, and Vivino record ID.

## Positioning

Unlike generic crowd-rating apps, this is a personal, parcel-accurate cartographic wine ledger: it pairs an interactive dual-layer map (**Terroirs & Parcels** vs **Tasting Places**) with a fast tasting log synced to the user's real Vivino cellar (`17` verified bottles and photos already on hand).

## Operating Context

Used on mobile during or right after a tasting (to log a bottle, rating, tasting note, and venue) and on desktop to browse the terroir map, compare Burgundy villages/climats, and sync with Vivino (`user_id: 77968357`, `cellar_id: 6491870`).

## Capabilities and Constraints

- Responsive desktop + mobile web interface (`web`, mobile-friendly viewport and touch targets).
- Dual-mode interactive physical-geography & terroir exposure map:
  1. **Карта терруаров, клима и экспозиции склонов (The World Atlas of Wine · 1:25 000)**: authentic *The World Atlas of Wine (7th & 9th Ed., pp. 50–75, 195, 270)* horizontal rotated Côte d'Or slope panorama (North `(N)→` to the right, wooded plateau `Woods / Bois` at top `350–425 м`, limestone slope in center `250–330 м`, and village communes below `210–245 м`), terracotta-red `5 м / 10 м` contour lines, tessellated *climat* polygons (`les Argillats`, `la Taupe / Combe d'Orveaux`, `Gevrey-Chambertin`, `Chambolle-Musigny`, `Vougeot`, `Monthélie`, `Meursault`, `Chassagne-Montrachet`, `Nantoux`, `Rully`, `Brouilly`, `Avize`, `NADAL`, `Верхнесадовое`), solar slope-exposure vectors (`ВЮВ 112°`, `ЮЮВ 158°`, `В 94°`, `ЮЗ 215°`), and an interactive geological cross-section profile (`Запад → Восток`, p. 51 *World Atlas of Wine*) — with zero artificial tasting-set lines or flight groupings.
  2. **Карта мест дегустации (Tasting Places Map)**: physical topography of Moscow (`120–195 м`) showing where and when each bottle was opened.
- Comprehensive **Энциклопедическая справка Wine Guide** inside the bottle dossier card: altitude (`м над ур. моря`), slope gradient (`%`), aspect (`ЮЮВ` / `ВЮВ`), geological stage (*Bathonian / Bajocian / Oxfordian / Campanian chalk*), microclimate, domain history, parcel/*climat* dossier, drinking window, serving temperature, glassware, food pairing, and reference source citation, plus a dedicated catalog of the 6 best Wine Guide & GIS sources.
- Built-in form to log a new wine (or edit rating/comment/tasting place of an existing bottle) with persistence (`localStorage` + JSON export + local Python Vivino sync helper).

## Brand Commitments

- **Committed visual world (`chartbook_geoeconomics` / Vintage Atlas Snowfall)**:
  - Parchment field `#F5F2E6` (`$color-paper`) with 80px surveyor's coordinate grid (`rgba(47, 41, 38, 0.03)`) and warm card surface `#FDF5E6` (`$color-paper-light`).
  - Ink `#2F2926` (`$color-ink`), secondary ink `#5A6263`, archival crimson `#8A0D2F` (`$color-red`), faded Prussian blue `#3B6E8F` (`$color-blue`), deep map-plate blue `#2C4F6B`, oxidised verdigris `#4A6B52` (`$color-green`), patina brass `#B8963E` (`$color-brass`), archival purple `#684182` (`$color-violet`).
  - Typography: `'SB Sans Interface'` (800 weight balanced headings, `tabular-nums` body and data tables) with `'Courier New'` monospace for catalog codes, coordinates, and Vivino IDs.
  - Card & plate physics: `2px solid #2F2926` borders, `8px` radius, hard-offset zero-blur shadows (`2px 2px 0px #3B6E8F, 4px 4px 0px #2F2926`), overprinted `.qcard-title` header bands, and brass keylines.
  - Cartographic styling (`cc.city.moscow_region.png` / `ru.xdata.tercontrol_map.png`): warm parchment land `#F3EDE0`, slope/terroir contour shading `#E3D9C6`, faded Prussian water `#A8BCC9` with `#7C98AB` stroke, sepia roads/borders `#C5B9A5`, crisp `1px solid #5A524C` neatline, L-shaped metric scale bar, and haloed place labels (`#FDF5E6` stroke).

## Evidence on Hand

- 17 real tasted wines synced with Vivino (`user_id: 77968357`, `cellar_id: 6491870`), documented in `WORKLOG — Gevrey-Chambertin & Vivino sync.md`.
- Real bottle label photos from chat uploads and `Camera Upload` (`Domaine Tortochot Gevrey-Chambertin VV 2018`, `Château de Laborde Hautes-Côtes de Beaune "En Cuillery" 2022`, `Rossignol-Cornu Hautes-Côtes de Beaune 2022`, `Moillard Gevrey-Chambertin "Beau Versant" 2021`, `Les Gamins d'Avize Blanc de Noirs`, `Nadal Original Reserva Brut Corpinnat`, `STN Трио Алиготе`, and the `burgundy.ru` 9-wine tasting card).

## Product Principles

1. **Parcel-level geographic truth**: never pin a Burgundy wine to a generic "France" marker — place every wine at its actual commune and *lieu-dit* / *climat* with soil, elevation, and vine-age context.
2. **Dual spatial memory**: switch effortlessly between *where the grapes grew* (Terroir layer) and *where the bottle was opened* (Tasting Places layer).
3. **One-screen utility on both desktop and phone**: logging a bottle, filtering by region/color/date, and flying to a parcel on the map work without page reloads.
