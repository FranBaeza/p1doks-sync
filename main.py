import json
import requests
from pathlib import Path
import time

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

#for pack in all_packs:
#    print(
#        f"{pack['Series']} | "
#        f"{pack['Car']} | "
#        f"{pack['Track']} | "
#       f"{pack['id']}"
#    )
    
    
# =========================
# DESCARGAR TODOS LOS ZIPS
# =========================

USER_ID = config["user_id"]

downloads_path = Path("downloads")
downloads_path.mkdir(exist_ok=True)

download_url = "https://api.p1doks.com/api/files/download-all"


for index, pack in enumerate(all_packs, start=1):

    print(
        f"\n[{index}/{len(all_packs)}] "
        f"Descargando: "
        f"{pack['Series']} | "
        f"{pack['Car']} | "
        f"{pack['Track']}"
    )

    # Nombre ZIP local
    filename = (
        f"{pack['Series']}-"
        f"{pack['Car']}-"
        f"S{pack['Season']}"
        f"W{pack['Week']}.zip"
    )

    # Limpiar caracteres problemáticos
    filename = filename.replace("/", "-")
    filename = filename.replace("\\", "-")
    filename = filename.replace(":", "-")

    zip_path = downloads_path / filename

    # Saltar si ya existe
    if zip_path.exists():
        print("  -> Ya existe, saltando")
        continue

    # Payload descarga
    download_payload = {
        "userId": USER_ID,
        "dataPackId": pack["id"],
        "dataPackName": (
            f"{pack['Series']}-"
            f"{pack['Year']}-"
            f"{pack['Car']}-"
            f"Season_{pack['Season']}-"
            f"Week_{pack['Week']}_"
            f"{pack['Track']}"
        )
    }

    # Request descarga
    try:

        response = requests.post(
            download_url,
            json=download_payload,
            headers=headers,
            timeout=60
        )

    except requests.exceptions.Timeout:
        print("  -> TIMEOUT")
        continue

    except Exception as e:
        print(f"  -> ERROR: {e}")
        continue

    if response.status_code == 401:
        print("  -> TOKEN EXPIRADO")
        break

    if response.status_code == 504:
        print("  -> SERVIDOR SATURADO")
        continue

    if response.status_code != 200:
        print(f"  -> ERROR {response.status_code}")
        continue

    # Guardar ZIP
    with open(zip_path, "wb") as f:
        f.write(response.content)
        
    time.sleep(1)
    
    print(f"  -> Guardado: {filename}")
    
with open("all_packs.json", "w", encoding="utf-8") as f:
    json.dump(all_packs, f, indent=4)