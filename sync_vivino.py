"""
Синхронизация личного винного атласа (wines_data.json) с аккаунтом Vivino.
Учётные данные читаются исключительно из локального C:\\Users\\timza\\.env (вне OneDrive).

Использование:
  python sync_vivino.py --check          # Проверить статус всех бутылок из wines_data.json в Vivino
  python sync_vivino.py --sync           # Записать новые бутылки и оценки из wines_data.json в погреб Vivino
  python sync_vivino.py --search "запрос" # Найти wine_id и vintage_id в каталоге Vivino (Algolia)
"""
import argparse
import json
import os
import re
from pathlib import Path
import requests

ENV_PATH = Path.home() / ".env"
DATA_PATH = Path(__file__).parent / "wines_data.json"

ALGOLIA_URL = "https://9takgwjuxl-dsn.algolia.net/1/indexes/WINES_prod/query"
ALGOLIA_HEADERS = {
    "X-Algolia-Application-Id": "9TAKGWJUXL",
    "X-Algolia-API-Key": "60c11b2f1068885161d95ca068d3a6ae",
    "Content-Type": "application/json",
}


def load_local_env():
    if not ENV_PATH.exists():
        raise RuntimeError(f"Файл окружения не найден: {ENV_PATH}")
    env_vars = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars


def search_vivino(query: str):
    r = requests.post(ALGOLIA_URL, headers=ALGOLIA_HEADERS, json={"query": query, "hitsPerPage": 8}, timeout=15)
    r.raise_for_status()
    hits = r.json().get("hits", [])
    for idx, h in enumerate(hits, 1):
        winery = (h.get("winery") or {}).get("name", "—")
        vintages = h.get("vintages") or []
        v_str = ", ".join(f"{v.get('year')}:{v.get('id')}" for v in vintages[:6])
        print(f"[{idx}] wine_id={h.get('id')} | {winery} — {h.get('name')} | vintages: {v_str}")


def create_vivino_session(email: str, password: str):
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
    })
    home = s.get("https://www.vivino.com/", timeout=20)
    m = re.search(r'name="csrf-token"\s+content="([^"]+)"', home.text)
    if not m:
        raise RuntimeError("Не удалось получить CSRF-токен Vivino")
    csrf = m.group(1)
    auth = s.post(
        "https://www.vivino.com/api/login",
        headers={"X-CSRF-Token": csrf, "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json"},
        json={"email": email, "password": password},
        timeout=20,
    )
    auth.raise_for_status()
    return s, csrf


def sync_collection(do_write: bool = False):
    env_vars = load_local_env()
    email = env_vars.get("VIVINO_EMAIL")
    password = env_vars.get("VIVINO_PASSWORD")
    if not email or not password:
        raise RuntimeError("В ~/.env не заданы VIVINO_EMAIL / VIVINO_PASSWORD")

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    cellar_id = data["account"]["cellar_id"]
    session, csrf = create_vivino_session(email, password)
    headers = {"X-CSRF-Token": csrf, "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json"}

    updated = False
    for w in data["wines"]:
        vid = w.get("vintage_id")
        if not vid:
            print(f"[ПРОПУСК] Нет vintage_id у бутылки: {w.get('producer')} — {w.get('name')}")
            continue
        check = session.get(f"https://www.vivino.com/api/vintages/{vid}/user_vintages", headers=headers, timeout=15)
        items = check.json().get("Change", []) if check.status_code == 200 else []
        if items:
            uv_id = items[0].get("id")
            w["user_vintage_id"] = uv_id
            print(f"[OK] В Vivino: {w['producer']} — {w['name']} ({w['vintage']}) -> user_vintage_id={uv_id}")
        elif do_write:
            # 1. Создаём запись в погребе
            c_res = session.post(
                f"https://www.vivino.com/api/cellars/{cellar_id}/vintages/{vid}",
                headers=headers,
                json={"bottle_State": "drank", "count": 1},
                timeout=15,
            )
            uv_res = session.post(
                f"https://www.vivino.com/api/vintages/{vid}/user_vintages",
                headers=headers,
                json={"vintage_id": vid, "rating": w.get("rating"), "note": w.get("notes") or ""},
                timeout=15,
            )
            if uv_res.status_code in (200, 201):
                uv_id = (uv_res.json().get("Change") or {}).get("id")
                w["user_vintage_id"] = uv_id
                updated = True
                print(f"[ДОБАВЛЕНО] {w['producer']} — {w['name']} -> user_vintage_id={uv_id} (cellar HTTP {c_res.status_code})")
        else:
            print(f"[НОВАЯ] Не синхронизирована: {w['producer']} — {w['name']} (vintage_id={vid})")

    if updated:
        DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Обновлён файл wines_data.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Синхронизация личного винного атласа с Vivino")
    parser.add_argument("--check", action="store_true", help="Проверить статус бутылок в Vivino")
    parser.add_argument("--sync", action="store_true", help="Записать новые бутылки в Vivino")
    parser.add_argument("--search", type=str, help="Поиск вина в каталоге Vivino (Algolia)")
    args = parser.parse_args()

    if args.search:
        search_vivino(args.search)
    elif args.sync:
        sync_collection(do_write=True)
    else:
        sync_collection(do_write=False)
