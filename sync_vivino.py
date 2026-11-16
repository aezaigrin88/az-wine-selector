"""
Двусторонняя синхронизация личного винного атласа (wines_data.json) с аккаунтом Vivino.
Поддерживает:
  1. Чтение учётных данных из переменных окружения (GitHub Actions Secrets:
     VIVINO_EMAIL, VIVINO_PASSWORD, VIVINO_COOKIE) или локального ~/.env.
  2. Импорт (Vivino -> wines_data.json): подтягивает новые отсканированные и оценённые
     вина из профиля и погреба Vivino (@artem_zaigrin, user_id=77968357, cellar_id=6491870),
     обогащает метаданные через каталог Vivino Algolia и геокодер OpenStreetMap Nominatim.
  3. Экспорт (wines_data.json -> Vivino): отправляет новые бутылки и оценки из дневника
     в погреб Vivino при наличии авторизованной сессии.
  4. Импорт из CSV-выгрузки Vivino (--import-csv full_wine_list.csv).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import requests

ENV_PATH = Path.home() / ".env"
DATA_PATH = Path(__file__).parent / "wines_data.json"

ALGOLIA_URL = "https://9takgwjuxl-dsn.algolia.net/1/indexes/WINES_prod/query"
ALGOLIA_HEADERS = {
    "X-Algolia-Application-Id": "9TAKGWJUXL",
    "X-Algolia-API-Key": "60c11b2f1068885161d95ca068d3a6ae",
    "Content-Type": "application/json",
}

VIVINO_TYPE_MAP: dict[int, tuple[str, str]] = {
    1: ("red", "Красное сухое"),
    2: ("white", "Белое сухое"),
    3: ("sparkling", "Шампанское / Игристое Брют"),
    4: ("rose", "Розовое сухое (Rosé)"),
    7: ("sweet", "Сладкое / Десертное / Креплёное"),
    24: ("sweet", "Сладкое / Десертное / Креплёное"),
}

COUNTRY_FALLBACK_COORDS: dict[str, tuple[float, float, str]] = {
    "france": (47.0525, 4.8350, "Франция"),
    "франция": (47.0525, 4.8350, "Франция"),
    "italy": (43.4633, 11.2558, "Италия"),
    "италия": (43.4633, 11.2558, "Италия"),
    "spain": (42.4627, -2.4450, "Испания"),
    "испания": (42.4627, -2.4450, "Испания"),
    "germany": (49.9189, 7.0694, "Германия"),
    "германия": (49.9189, 7.0694, "Германия"),
    "austria": (48.4092, 15.6142, "Австрия"),
    "австрия": (48.4092, 15.6142, "Австрия"),
    "south africa": (-33.9321, 18.8602, "ЮАР"),
    "юар": (-33.9321, 18.8602, "ЮАР"),
    "russia": (44.8321, 37.3771, "Россия"),
    "россия": (44.8321, 37.3771, "Россия"),
    "argentina": (-33.3562, -69.1647, "Аргентина"),
    "chile": (-33.5931, -70.6991, "Чили"),
    "united states": (38.5025, -122.2654, "США"),
    "portugal": (41.1621, -7.7892, "Португалия"),
    "new zealand": (-41.5134, 173.9612, "Новая Зеландия"),
    "australia": (-34.5562, 138.9589, "Австралия"),
}


def load_credentials() -> dict[str, str]:
    creds: dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip().strip('"').strip("'")
    for env_key in ("VIVINO_EMAIL", "VIVINO_PASSWORD", "VIVINO_COOKIE"):
        val = (os.environ.get(env_key) or "").strip()
        if val:
            creds[env_key] = val
    return creds


def refine_wine_style(base_style: str, base_label: str, text_pool: str) -> tuple[str, str]:
    t = text_pool.lower()
    if base_style == "sparkling" or re.search(
        r"\b(champagne|cr[ée]mant|cava|corpinnat|prosecco|franciacorta|spumante|sekt|brut|asti)\b"
        r"|blanc\s+de\s+(blancs|noirs)|p[ée]t[\s-]*nat"
        r"|шампанск[а-яё]*|игрист[а-яё]*|блан\s+де\s+(блан|нуар)|брют|креман|просекко|кава|асти",
        t,
    ):
        if re.search(r"blanc\s+de\s+blancs|блан\s+де\s+блан", t):
            return "sparkling_bdb", "Блан де Блан / Blanc de Blancs"
        if re.search(r"blanc\s+de\s+noirs|блан\s+де\s+нуар", t):
            return "sparkling_bdn", "Блан де Нуар / Blanc de Noirs"
        if re.search(r"\b(ros[ée]|rosato|rosado)\b|розов[а-яё]*", t):
            return "sparkling_rose", "Розовое шампанское / Brut Rosé"
        if re.search(r"brut\s+nature|zero\s+dosage|брют\s+натюр|зеро\s+дозаж", t):
            return "sparkling_brut_nature", "Брют Натюр / Зеро Дозаж"
        if re.search(r"extra[\s-]*brut|экстра\s+брют", t):
            return "sparkling_extra_brut", "Экстра Брют"
        if re.search(r"prosecco|просекко|asti|асти|p[ée]t[\s-]*nat", t):
            return "sparkling_prosecco", "Просекко / Пет-нат / Асти"
        if re.search(r"cr[ée]mant|креман|cava|кава|corpinnat|корпиннат|franciacorta|франчакорта", t):
            return "sparkling_cremant", "Креман / Кава / Корпиннат / Франчакорта"
        if re.search(r"demi[\s-]*sec|полусух[а-яё]*|полусладк[а-яё]*", t):
            return "sparkling_demi_sec", "Игристое Полусухое / Деми-Сек"
        return "sparkling", "Шампанское / Игристое Брют"

    if base_style == "rose" or (
        not base_style and re.search(r"\b(ros[ée]|rosato|rosado)\b|розов[а-яё]*", t)
    ):
        return "rose", "Розовое сухое (Rosé)"
    if re.search(r"\b(orange\s+wine|skin\s+contact|amber\s+wine|qvevri)\b|оранжев[а-яё]*|квеври", t):
        return "orange", "Оранжевое / Амбер"
    if base_style == "sweet" or re.search(r"\b(sauternes|tokaji|icewine|eiswein|port|porto|sherry)\b", t):
        return "sweet", "Сладкое / Десертное / Креплёное"
    if base_style == "white" or (
        not base_style
        and re.search(
            r"\b(chardonnay|sauvignon\s+blanc|chenin\s+blanc|riesling|aligot[ée]|pinot\s+gris|pinot\s+grigio|gr[üu]ner\s+veltliner|viognier|albari[ñn]o|chablis|meursault|puligny|sancerre)\b|бел[а-яё]*",
            t,
        )
    ):
        return "white", "Белое сухое"
    return base_style or "red", base_label or "Красное сухое"


def geocode_region(commune: str, region: str, country: str, cache: dict[str, tuple[float, float]]) -> tuple[float, float]:
    key = " | ".join(part for part in (commune, region, country) if part).strip().lower()
    if key in cache:
        return cache[key]

    queries = [q for q in (f"{commune}, {region}, {country}".strip(", "), f"{region}, {country}".strip(", ")) if q]
    for q in queries:
        try:
            time.sleep(1.05)
            resp = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": q, "format": "json", "limit": 1},
                headers={"User-Agent": "AZ-Wine-Diary-Sync/1.0 (github.com/aezaigrin88/az-wine-selector)"},
                timeout=10,
            )
            if resp.status_code == 200:
                arr = resp.json()
                if isinstance(arr, list) and arr:
                    lat = round(float(arr[0]["lat"]), 5)
                    lon = round(float(arr[0]["lon"]), 5)
                    cache[key] = (lat, lon)
                    return lat, lon
        except Exception:
            pass

    c_low = (country or "").strip().lower()
    if c_low in COUNTRY_FALLBACK_COORDS:
        lat, lon, _ = COUNTRY_FALLBACK_COORDS[c_low]
        cache[key] = (lat, lon)
        return lat, lon
    return 47.0525, 4.8350


def query_algolia_single(query: str) -> dict[str, Any] | None:
    if not query.strip():
        return None
    try:
        r = requests.post(
            ALGOLIA_URL,
            headers=ALGOLIA_HEADERS,
            json={"query": query.strip(), "hitsPerPage": 5},
            timeout=15,
        )
        if r.status_code == 200:
            hits = r.json().get("hits") or []
            return hits[0] if hits else None
    except Exception:
        pass
    return None


def search_vivino(query: str) -> None:
    r = requests.post(ALGOLIA_URL, headers=ALGOLIA_HEADERS, json={"query": query, "hitsPerPage": 8}, timeout=15)
    r.raise_for_status()
    hits = r.json().get("hits", [])
    for idx, h in enumerate(hits, 1):
        winery = (h.get("winery") or {}).get("name", "-")
        vintages = h.get("vintages") or []
        v_str = ", ".join(f"{v.get('year')}:{v.get('id')}" for v in vintages[:6])
        print(f"[{idx}] wine_id={h.get('id')} | {winery} · {h.get('name')} | vintages: {v_str}")


def create_vivino_session(creds: dict[str, str]) -> tuple[requests.Session, dict[str, str], bool]:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
        }
    )
    api_headers = {"X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json"}

    raw_cookie = creds.get("VIVINO_COOKIE", "").strip()
    if raw_cookie:
        if "=" in raw_cookie:
            for pair in raw_cookie.split(";"):
                if "=" in pair:
                    ck, cv = pair.strip().split("=", 1)
                    s.cookies.set(ck.strip(), cv.strip(), domain=".vivino.com")
        else:
            s.cookies.set("_vivino_session", raw_cookie, domain=".vivino.com")

    try:
        home = s.get("https://www.vivino.com/", timeout=20)
        m = re.search(r'name="csrf-token"\s+content="([^"]+)"', home.text or "")
        if m:
            api_headers["X-CSRF-Token"] = m.group(1)
    except Exception as exc:
        print(f"[INFO] Не удалось открыть главную страницу Vivino: {exc}")
        return s, api_headers, bool(raw_cookie)

    if raw_cookie:
        return s, api_headers, True

    email = creds.get("VIVINO_EMAIL", "").strip()
    password = creds.get("VIVINO_PASSWORD", "").strip()
    if not email or not password:
        print("[INFO] Секреты VIVINO_EMAIL / VIVINO_PASSWORD не заданы — работаем в публичном режиме чтения.")
        return s, api_headers, False

    if "X-CSRF-Token" not in api_headers:
        print("[INFO] Vivino не вернул CSRF-токен (возможна защита Cloudflare в ЦОД) — используем публичный режим + Algolia.")
        return s, api_headers, False

    try:
        auth = s.post(
            "https://www.vivino.com/api/login",
            headers=api_headers,
            json={"email": email, "password": password},
            timeout=20,
        )
        if auth.status_code in (200, 201):
            print("[OK] Авторизация в Vivino выполнена.")
            return s, api_headers, True
        print(f"[INFO] Авторизация Vivino вернула HTTP {auth.status_code} — продолжаем в режиме чтения.")
    except Exception as exc:
        print(f"[INFO] Ошибка авторизации Vivino ({exc}) — продолжаем в режиме чтения.")
    return s, api_headers, False


def build_wine_record_from_vivino_item(
    raw_item: dict[str, Any],
    next_id: int,
    geo_order: int,
    geo_cache: dict[str, tuple[float, float]],
) -> dict[str, Any] | None:
    vintage_obj = raw_item.get("vintage") or raw_item
    wine_obj = vintage_obj.get("wine") or raw_item.get("wine") or {}
    winery_obj = wine_obj.get("winery") or vintage_obj.get("winery") or {}
    region_obj = wine_obj.get("region") or vintage_obj.get("region") or {}
    country_obj = region_obj.get("country") or wine_obj.get("country") or {}

    producer = (winery_obj.get("name") or raw_item.get("producer") or "").strip()
    wine_name = (wine_obj.get("name") or vintage_obj.get("name") or raw_item.get("name") or "").strip()
    year_raw = str(vintage_obj.get("year") or raw_item.get("vintage") or "").strip()
    if year_raw in ("", "0", "None", "N.V.", "NV", "U.V."):
        vintage_str = "N.V."
    else:
        vintage_str = year_raw

    if not producer and not wine_name:
        return None
    if not producer:
        producer = wine_name

    wine_id = wine_obj.get("id") or raw_item.get("wine_id")
    vintage_id = vintage_obj.get("id") or raw_item.get("vintage_id")
    user_vintage_id = raw_item.get("id") if "vintage" in raw_item else raw_item.get("user_vintage_id")

    alg_hit = None
    if not region_obj or not wine_obj.get("type_id"):
        alg_hit = query_algolia_single(f"{producer} {wine_name}")
        if alg_hit:
            wine_id = wine_id or alg_hit.get("id")
            if not region_obj and isinstance(alg_hit.get("region"), dict):
                region_obj = alg_hit["region"]
                country_obj = region_obj.get("country") or country_obj

    type_id = int((wine_obj.get("type_id") or (alg_hit or {}).get("type_id") or 0) or 0)
    base_style, base_label = VIVINO_TYPE_MAP.get(type_id, ("", ""))
    region_name = (region_obj.get("name") or raw_item.get("region") or "").strip()
    country_raw = (country_obj.get("name") or raw_item.get("country") or "").strip()
    c_info = COUNTRY_FALLBACK_COORDS.get(country_raw.lower())
    country_ru = c_info[2] if c_info else country_raw

    grapes_list = wine_obj.get("grapes") or (alg_hit or {}).get("grapes") or []
    grape_names: list[str] = []
    for g in grapes_list:
        if isinstance(g, dict) and g.get("name"):
            grape_names.append(str(g["name"]))
        elif isinstance(g, str):
            grape_names.append(g)
    grapes_str = ", ".join(grape_names[:4])

    style_code, style_label = refine_wine_style(
        base_style,
        base_label,
        f"{producer} {wine_name} {region_name} {grapes_str} {raw_item.get('regional_style', '')}",
    )

    lat, lon = geocode_region(region_name, region_name, country_raw or country_ru, geo_cache)

    stats = vintage_obj.get("statistics") or wine_obj.get("statistics") or (alg_hit or {}).get("statistics") or {}
    vivino_avg = stats.get("ratings_average") or raw_item.get("vivino_avg")
    if vivino_avg is not None:
        try:
            vivino_avg = round(float(vivino_avg), 1)
        except Exception:
            vivino_avg = None

    user_rating = raw_item.get("rating")
    if user_rating is not None and user_rating != "":
        try:
            user_rating = round(float(user_rating), 2)
            if user_rating <= 0:
                user_rating = None
        except Exception:
            user_rating = None
    else:
        user_rating = None

    created_raw = str(raw_item.get("created_at") or raw_item.get("tasted_date") or "").strip()
    tasted_date = created_raw[:10] if re.match(r"^\d{4}-\d{2}-\d{2}", created_raw) else dt.date.today().isoformat()

    image_obj = vintage_obj.get("image") or (alg_hit or {}).get("image") or {}
    variations = image_obj.get("variations") or {}
    img_url = (
        variations.get("bottle_large")
        or variations.get("bottle_medium")
        or image_obj.get("location")
        or ""
    )
    if isinstance(img_url, str) and img_url.startswith("//"):
        img_url = "https:" + img_url

    default_bottle = (
        "img/labels/bottle_02.png"
        if style_code.startswith("sparkling")
        else ("img/labels/bottle_05.png" if style_code == "white" else "img/labels/bottle_17.png")
    )
    bottle_studio = img_url or default_bottle

    viv_url = (
        raw_item.get("vivino_url")
        or (f"https://www.vivino.com/wines/{vintage_id}" if vintage_id else None)
    )

    return {
        "id": next_id,
        "_uid": f"vivino_{vintage_id or wine_id or next_id}",
        "_updatedAt": int(time.time() * 1000),
        "_userEdited": True,
        "wine_id": int(wine_id) if str(wine_id or "").isdigit() else None,
        "vintage_id": int(vintage_id) if str(vintage_id or "").isdigit() else None,
        "user_vintage_id": int(user_vintage_id) if str(user_vintage_id or "").isdigit() else None,
        "producer": producer,
        "name": wine_name or producer,
        "vintage": vintage_str,
        "style": style_code,
        "style_label": style_label,
        "grapes": grapes_str,
        "abv": "",
        "country": country_ru,
        "macro_region": region_name,
        "sub_region": region_name,
        "commune": region_name,
        "lieu_dit": "",
        "lat": lat,
        "lon": lon,
        "elevation": "",
        "soil": "",
        "vine_age": "",
        "aging": "",
        "rating": user_rating,
        "rating_az": user_rating,
        "rating_anya": None,
        "vivino_avg": vivino_avg,
        "notes": str(raw_item.get("note") or raw_item.get("review") or "").strip(),
        "vivino_url": viv_url,
        "bottle_studio": bottle_studio,
        "photos": [bottle_studio],
        "appellation_rank": region_name,
        "geo_order": geo_order,
        "terroir_tier": "village_cotedor",
        "tasted_date": tasted_date,
        "purchased_at": "",
        "guide_source": "Импорт из профиля Vivino (@artem_zaigrin)",
    }


def fetch_vivino_user_items(session: requests.Session, headers: dict[str, str], user_id: int, cellar_id: int) -> list[dict[str, Any]]:
    collected: list[dict[str, Any]] = []
    seen_keys: set[str] = set()

    endpoints = [
        f"https://www.vivino.com/api/users/{user_id}/user_vintages?per_page=50&page=1&order_by=created_at&order=desc",
        f"https://www.vivino.com/api/cellars/{cellar_id}/vintages?per_page=50&page=1",
    ]
    for url in endpoints:
        try:
            resp = session.get(url, headers=headers, timeout=18)
            if resp.status_code != 200:
                continue
            payload = resp.json()
            rows = (
                payload.get("user_vintages")
                or payload.get("Change")
                or payload.get("cellar_vintages")
                or payload.get("records")
                or (payload if isinstance(payload, list) else [])
            )
            if not isinstance(rows, list):
                continue
            for item in rows:
                if not isinstance(item, dict):
                    continue
                v = item.get("vintage") or item
                vid = v.get("id") or item.get("vintage_id")
                key = str(vid or item.get("id") or "")
                if key and key not in seen_keys:
                    seen_keys.add(key)
                    collected.append(item)
        except Exception as exc:
            print(f"[INFO] Пропуск ответа {url}: {exc}")
    return collected


def import_from_csv(csv_path: Path, data: dict[str, Any]) -> int:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV-файл не найден: {csv_path}")
    deleted_map = (data.get("account") or {}).get("deleted_wine_map") or {}
    existing_wines = data.get("wines") or []
    geo_cache: dict[str, tuple[float, float]] = {}
    added = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            producer = (row.get("Winery") or row.get("Producer") or "").strip()
            name = (row.get("Wine name") or row.get("Wine") or "").strip()
            vintage = (row.get("Vintage") or "").strip() or "N.V."
            if not producer and not name:
                continue
            link = (row.get("Link to wine") or "").strip()
            vid_match = re.search(r"/wines/(\d+)", link)
            vid = int(vid_match.group(1)) if vid_match else None

            already = any(
                (vid and w.get("vintage_id") == vid)
                or (
                    str(w.get("producer", "")).lower() == producer.lower()
                    and str(w.get("name", "")).lower() == name.lower()
                    and str(w.get("vintage", "")).lower() == vintage.lower()
                )
                for w in existing_wines
            )
            if already:
                continue

            next_id = max([0, *[int(w.get("id") or 0) for w in existing_wines]]) + 1
            if str(next_id) in deleted_map:
                next_id += 1

            rec = build_wine_record_from_vivino_item(
                {
                    "producer": producer,
                    "name": name,
                    "vintage": vintage,
                    "vintage_id": vid,
                    "region": row.get("Region") or "",
                    "country": row.get("Country") or "",
                    "regional_style": row.get("Regional wine style") or "",
                    "vivino_avg": row.get("Average rating") or None,
                    "rating": row.get("Your rating") or None,
                    "note": row.get("Your review") or row.get("Personal Note") or "",
                    "tasted_date": row.get("Scan date") or "",
                    "vivino_url": link or None,
                },
                next_id=next_id,
                geo_order=len(existing_wines) + 1,
                geo_cache=geo_cache,
            )
            if rec:
                existing_wines.insert(0, rec)
                added += 1
                print(f"[CSV ИМПОРТ] +{rec['id']}: {rec['producer']} · {rec['name']} ({rec['vintage']})")
    return added


def sync_collection(do_pull: bool = True, do_push: bool = False, csv_file: str | None = None) -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    account = data.setdefault("account", {})
    user_id = int(account.get("user_id") or 77968357)
    cellar_id = int(account.get("cellar_id") or 6491870)
    deleted_map = account.get("deleted_wine_map") or {}

    updated = False

    if csv_file:
        added_csv = import_from_csv(Path(csv_file), data)
        if added_csv > 0:
            updated = True

    creds = load_credentials()
    session, headers, is_authed = create_vivino_session(creds)
    geo_cache: dict[str, tuple[float, float]] = {}

    if do_pull:
        remote_items = fetch_vivino_user_items(session, headers, user_id, cellar_id)
        if remote_items:
            print(f"[OK] Получено записей из профиля Vivino: {len(remote_items)}")
        for item in remote_items:
            v_obj = item.get("vintage") or item
            w_obj = v_obj.get("wine") or item.get("wine") or {}
            vid = v_obj.get("id") or item.get("vintage_id")
            wid = w_obj.get("id") or item.get("wine_id")
            uv_id = item.get("id") if "vintage" in item else item.get("user_vintage_id")
            v_year = str(v_obj.get("year") or "").strip()

            match = None
            for existing in data["wines"]:
                if (uv_id and existing.get("user_vintage_id") == uv_id) or (
                    vid and existing.get("vintage_id") == vid
                ):
                    match = existing
                    break
                if wid and existing.get("wine_id") == wid and str(existing.get("vintage") or "") == v_year:
                    match = existing
                    break

            if match is not None:
                r_val = item.get("rating")
                if r_val and match.get("rating_az") in (None, ""):
                    try:
                        rf = round(float(r_val), 2)
                        if rf > 0:
                            match["rating_az"] = rf
                            match["rating"] = rf
                            match["_updatedAt"] = int(time.time() * 1000)
                            updated = True
                            print(f"[ОБНОВЛЕНА ОЦЕНКА] {match.get('producer')} · {match.get('name')} -> {rf}")
                    except Exception:
                        pass
                note_val = str(item.get("note") or "").strip()
                if note_val and not match.get("notes"):
                    match["notes"] = note_val
                    match["_updatedAt"] = int(time.time() * 1000)
                    updated = True
                continue

            # Пропускаем бутылки, явно удалённые пользователем по vintage_id
            if vid and any(str(vid) == str(dv) for dv in account.get("deleted_vintage_ids", [])):
                continue

            next_id = max([19, *[int(w.get("id") or 0) for w in data["wines"]]]) + 1
            while str(next_id) in deleted_map:
                next_id += 1

            rec = build_wine_record_from_vivino_item(
                item,
                next_id=next_id,
                geo_order=len(data["wines"]) + 1,
                geo_cache=geo_cache,
            )
            if rec:
                data["wines"].insert(0, rec)
                updated = True
                print(f"[ИМПОРТ ИЗ VIVINO] #{rec['id']}: {rec['producer']} · {rec['name']} ({rec['vintage']})")

    if do_push and is_authed:
        for w in data["wines"]:
            vid = w.get("vintage_id")
            if not vid:
                continue
            try:
                check = session.get(f"https://www.vivino.com/api/vintages/{vid}/user_vintages", headers=headers, timeout=15)
                items = check.json().get("Change", []) if check.status_code == 200 else []
            except Exception:
                items = []
            if items:
                uv_id = items[0].get("id")
                if uv_id and w.get("user_vintage_id") != uv_id:
                    w["user_vintage_id"] = uv_id
                    updated = True
                continue

            c_res = session.post(
                f"https://www.vivino.com/api/cellars/{cellar_id}/vintages/{vid}",
                headers=headers,
                json={"bottle_State": "drank", "count": 1},
                timeout=15,
            )
            eff_rating = w.get("rating_az") if w.get("rating_az") is not None else w.get("rating")
            uv_res = session.post(
                f"https://www.vivino.com/api/vintages/{vid}/user_vintages",
                headers=headers,
                json={"vintage_id": vid, "rating": eff_rating, "note": w.get("notes") or ""},
                timeout=15,
            )
            if uv_res.status_code in (200, 201):
                uv_id = (uv_res.json().get("Change") or {}).get("id")
                w["user_vintage_id"] = uv_id
                updated = True
                print(f"[ЭКСПОРТ В VIVINO] {w['producer']} · {w['name']} -> user_vintage_id={uv_id} (cellar HTTP {c_res.status_code})")

    if updated:
        account["last_synced"] = dt.date.today().isoformat()
        account["updated_at_ms"] = int(time.time() * 1000)
        DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("[OK] Обновлён файл wines_data.json")
    else:
        print("[OK] Новых изменений для записи в wines_data.json нет.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Двусторонняя синхронизация AZ Wine Diary с Vivino")
    parser.add_argument("--check", action="store_true", help="Только чтение и импорт новых вин из Vivino")
    parser.add_argument("--sync", action="store_true", help="Экспорт новых бутылок из дневника в Vivino")
    parser.add_argument("--bidirectional", action="store_true", help="Двусторонняя синхронизация (импорт из Vivino + экспорт в Vivino)")
    parser.add_argument("--import-csv", type=str, default=None, help="Путь к CSV-выгрузке из Vivino (full_wine_list.csv)")
    parser.add_argument("--search", type=str, help="Поиск вина в каталоге Vivino (Algolia)")
    args = parser.parse_args()

    if args.search:
        search_vivino(args.search)
    elif args.bidirectional:
        sync_collection(do_pull=True, do_push=True, csv_file=args.import_csv)
    elif args.sync:
        sync_collection(do_pull=False, do_push=True, csv_file=args.import_csv)
    else:
        sync_collection(do_pull=True, do_push=False, csv_file=args.import_csv)
