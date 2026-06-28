import json
import requests
from downloader import download_packs
from selection_engine import build_download_queue

# Cargar config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config["bearer_token"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# =========================
# OBTENER TODOS LOS DATAPACKS
# =========================

url = "https://api.p1doks.com/ql/data-packs"

limit = 20
offset = 0

all_packs = []

while True:

    payload = {
        "limit": limit,
        "offset": offset,
        "filters": {
            "Year": {"_eq": str(config["year"])},
            "Week": {"_eq": str(config["week"])},
            "Season": {"_eq": str(config["season"])}
        },
        "sort": [
            "lap_minutes",
            "lap_seconds",
            "lap_hundredths"
        ]
    }

    try:

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=60
        )

    except requests.exceptions.Timeout:
        print("  -> TIMEOUT obteniendo datapacks")
        continue

    except Exception as e:
        print(f"  -> ERROR obteniendo datapacks: {e}")
        continue

    if response.status_code != 200:
        print(f"  -> ERROR {response.status_code} obteniendo datapacks")
        break


    data = response.json()

    packs = data["data_pack"]

    if not packs:
        break

    all_packs.extend(packs)

    print(f"Página offset={offset} -> {len(packs)} packs")

    offset += limit

print(f"\nTOTAL PACKS: {len(all_packs)}")


# =========================
# MOSTRAR TODOS LOS DATAPACKS
# =========================

for pack in all_packs:
    print(
        f"{pack['Series']} | "
        f"{pack['Car']} | "
        f"{pack['Track']} | "
        f"{pack['id']}"
    )

from selection import build_profile

download_queue = build_profile(
    all_packs,
    config["download_profile"]
)
    
download_packs(
    download_queue,
    config,
    headers
)
    
with open("all_packs.json", "w", encoding="utf-8") as f:
    json.dump(all_packs, f, indent=4)