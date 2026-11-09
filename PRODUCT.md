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

Unlike generic crowd-rating apps, this is a personal, parcel-accurate cartographic wine ledger (**AZ Wine Diary**): it pairs a strict North-Up (`N ↑`) 4-level semantic terroir map (**Leaflet 1.9.4 + OpenStreetMap + INAO/DGFiP cadastre**) with a 3-stage photo/barcode/web bottle recognition pipeline and dual personal tasting scores for Artem and Anya.

## Operating Context

Used on mobile (iPhone PWA) during or right after a tasting (to scan a bottle label + back label + barcode, enrich from live web sources, and log Artem & Anya's 4-component ratings) and on desktop to browse the world terroir map, compare communes/*climats*, and sync with `G:\My Drive\az-AI\Wine` and GitHub Pages (`https://aezaigrin88.github.io/az-wine-selector/`).

## Capabilities and Constraints

- Responsive desktop + mobile PWA (`index.html` + `manifest.webmanifest`, mobile-friendly viewport and touch targets).
- Strict **North-Up (`N ↑`)** 4-level semantic physical-geography & terroir map (`terroir_atlas_geojson.js`):
  1. **Level 1 (`Z2–Z4`)**: Wine-producing countries and global diary collection overview.
  2. **Level 2 (`Z5–Z7`)**: Physical terrain relief and macro wine regions across Europe, Russia/Crimea/Kuban, Americas, South Africa, and Oceania.
  3. **Level 3 (`Z8–Z11`)**: Sub-regions and appellations (Côte de Nuits, Côte de Beaune, Côte Chalonnaise, Beaujolais, Champagne, Bordeaux, Penedès, Kuban, Crimea, Mendoza, Western Cape, etc.).
  4. **Level 4 (`Z12–Z17`)**: Cadastral parcels 1:25 000 (`9 586` authentic DGFiP/INAO *lieux-dits* and OpenStreetMap vineyard polygons), SRTM elevation contours, and solar slope-exposure vectors (`☀️`).
- **3-Stage Zero-Patch Bottle Recognition & Web Enrichment Pipeline**:
  - **Stage 1 (OCR + Barcode)**: iOS WebKit OOM-safe downscaling (`<= 920px` JPEG) with a single shared `Tesseract.createWorker("rus+eng")` and rotated barcode decoding (`jsQR` + `ZXing`), extracting grape variety (`GRAPE_VARIETY_DICTIONARY`), ABV, dosage, vintage (`1980–2026` or `N.V.`), postal commune, and official appellation (`extractUniversalAppellationInfo`).
  - **Stage 2 (User Supplementation)**: Optional one-field refinement of Producer or Cuvée.
  - **Stage 3 (`runStage3DeepWebBottleEnrichment`)**: Parallel live lookup across **OpenFoodFacts ElasticSearch API**, **Vivino Search**, **Bing/DuckDuckGo `site:vivino.com`**, and **Multi-Language Wikipedia/Wikidata** (`en/fr/es/it/de/ru`).
- **Single Source of Truth (`wines_data.json`)**: All canonical bottle attributes (`commune_code`, `cadastral_lieu_dit`, `osm_way_id`, `parcel_tier`, `elevation_m`, ratings, and tasting dossiers) live declaratively in `wines_data.json` and are loaded directly by `index.html`.

## Brand Commitments

- **Committed visual world (`Vintage Atlas` / Cartographer's Cellar Ledger)**:
  - Parchment field `#F5F2E6` with warm card surface `#FDF5E6` and toolbar strip `#EFEAD8`.
  - Ink `#2F2926`, secondary ink `#484E4F`, archival crimson `#8A0D2F` (Red wines), faded Prussian blue `#3B6E8F` (White wines), deep map-plate blue `#2C4F6B`, oxidised verdigris `#4A6B52`, burnt amber `#C85A17` (Sparkling wines), patina brass `#B8963E`.
  - System & editorial typography: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` (`tabular-nums` for vintages, ABV, ratings, and coordinates) with `'Courier New', monospace` for catalog codes and coordinates.

## Evidence on Hand

- Canonical collection in [`wines_data.json`](file:///G:/My%20Drive/az-AI/Wine/wines_data.json) (`18` tasted bottles across Burgundy, Champagne, Bordeaux, Penedès, Sevastopol/Belbek, and Kuban/Semisam) and continuous ledger [`WORKLOG — AZ Wine Diary.md`](file:///G:/My%20Drive/az-AI/Wine/WORKLOG%20—%20AZ%20Wine%20Diary.md).

## Product Principles

1. **Parcel-level geographic truth (`Zero-Patch`)**: never hardcode bottle-specific `if` branches in code — resolve every wine declaratively via `wines_data.json`, INAO/DGFiP cadastre, and `WORLD_WINE_REGIONS`.
2. **Dynamic Taste Compass**: rank favorite communes, styles, and next-step terroir recommendations dynamically from Artem and Anya's 4-component tasting scores (`Аромат`, `Баланс во вкусе`, `Послевкусие`, `Сложность`).
3. **One-screen utility on both desktop and phone**: scanning a bottle, filtering by region/color/rating, and flying to a parcel on the map work without page reloads.
