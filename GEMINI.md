# Правила проекта `Wine` (`az-wine-selector` · `Whitelist-Only` & `Zero-Patch`)

## 1. Назначение и белый список проекта `Wine`
- **Папка в Google Drive (`📁` / `☁️`)**: [`G:\My Drive\az-AI\Wine`](file:///G:/My%20Drive/az-AI/Wine) (Drive ID: `1_6mDlBXTeEEGpN-iknWGT9OZgMUtP97l`)
- **GitHub-репозиторий (`☁️`)**: [`aezaigrin88/az-wine-selector`](https://github.com/aezaigrin88/az-wine-selector) ([GitHub Pages](https://aezaigrin88.github.io/az-wine-selector/))
- **Сводный индекс проекта**: [`WORKLOG.md`](./WORKLOG.md) (Drive ID: `1RU9okUPOZBkzu68z0Iag2wxQVmwptNCw`)

## 2. Белые списки активных диалогов проекта (`Whitelist`)
1. **`📱 AZ Wine Diary`** (`☁️ 🍷 Wine`, главный диалог приложения, сквозной журнал `#1..#98`): [`WORKLOG — AZ Wine Diary.md`](./WORKLOG%20%E2%80%94%20AZ%20Wine%20Diary.md) — веб-приложение `index.html`, декларативная база `wines_data.json`, геоданные терруаров `terroir_atlas_geojson.js`, генератор кадастра `codex/build_authentic_terroir_geojson.py`, `sync_vivino.py`, `PRODUCT.md`, `DESIGN.md` и новогодний гид-отбор `new_year_wine_bank_selection.md` (`14x_C86s9bWled6mXHRG5IKEjpRYPAoOJ`).
2. **`Champagne selection`**: [`WORKLOG — Champagne selection.md`](./WORKLOG%20%E2%80%94%20Champagne%20selection.md) (`1kIyGHwrNDtvYKJRIIjHootJVMCNJA9Ps`) — отбор и дегустационные разборы шампанских и игристых вин (`champagne_analysis.md`, `discussion_champagne_wine.md`).
3. **`Serials About Wine And Geography`**: [`WORKLOG — Serials About Wine And Geography.md`](./WORKLOG%20%E2%80%94%20Serials%20About%20Wine%20And%20Geography.md) (`1Rvvx6ajfY1kk9bM8SzyMZudwjaBDQre9`) — подборка фильмов, сериалов и книг о вине и географии (`year_in_burgundy_domaines.md`).

## 3. Архитектурный стандарт `Zero-Patch` для `AZ Wine Diary` (`az-wine-selector`)
1. **Единый источник истины (`Single Source of Truth`)**: все атрибуты вин (`commune_code`, `lieu_dit`, `osm_way_id`, `elevation_m`, `parcel_tier`, оценки и заметки) хранятся декларативно в `wines_data.json`. Запрещено хардкодить `if wid == X:` или `if wid_osm == Y:` внутри `build_authentic_terroir_geojson.py` или `index.html`.
2. **Каноническая классификация терруаров**: ранг парцеля (`Grand Cru` / `Premier Cru` / `Village`) определяется только по официальному реестру INAO / кадастру аппелласьона или полю `appellation_rank`, а не по порядковому номеру площади полигона (`idx < 45`) или костылям по долготе/широте.
3. **Синхронизация 50/50 (`☁️` / `📁`)**: в начале облачной сессии скачивать свежие файлы из Google Drive (`gdrive readonly download`), а после правок — обновлять в Google Drive (`gdrive mutate update`) и пушить в `aezaigrin88/az-wine-selector`.
