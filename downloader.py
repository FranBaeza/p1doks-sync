import requests
import time
from pathlib import Path


def download_packs(
    download_queue,
    config,
    headers
):

    user_id = config["user_id"]

    downloads_path = Path("downloads")
    downloads_path.mkdir(exist_ok=True)

    download_url = "https://api.p1doks.com/api/files/download-all"

    max_downloads = config["max_downloads_per_day"]
    downloads_today = 0

    print("\n==============================")
    print("INICIANDO DESCARGAS")
    print("==============================")

    for group in download_queue:

        rule = group["rule"]
        packs = group["packs"]

        needed = rule["count"]
        downloaded = 0

        print("\n--------------------------------")
        print(f"Regla: {rule}")
        print(f"Objetivo: {needed} descargas nuevas")
        print("--------------------------------")

        for pack in packs:

            # Límite global diario
            if downloads_today >= max_downloads:

                print(f"\nLímite diario alcanzado ({max_downloads}).")
                return

            # Regla completada
            if downloaded >= needed:
                break

            print(
                f"\n[{downloads_today + 1}/{max_downloads}] "
                f"{pack['Series']} | "
                f"{pack['Car']} | "
                f"{pack['Track']}"
            )

            filename = (
                f"{pack['Series']}-"
                f"{pack['Car']}-"
                f"S{pack['Season']}"
                f"W{pack['Week']}.zip"
            )

            filename = (
                filename
                .replace("/", "-")
                .replace("\\", "-")
                .replace(":", "-")
            )

            zip_path = downloads_path / filename

            # Ya descargado anteriormente
            if zip_path.exists():

                print("  -> Ya existe")

                continue

            download_payload = {

                "userId": user_id,

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

                return

            if response.status_code == 504:

                print("  -> SERVIDOR SATURADO")

                continue

            if response.status_code != 200:

                print(f"  -> ERROR {response.status_code}")

                continue

            with open(zip_path, "wb") as f:

                f.write(response.content)

            downloads_today += 1
            downloaded += 1

            time.sleep(1)

            print(
                f"  -> Guardado ({downloaded}/{needed}) "
                f"[Global {downloads_today}/{max_downloads}]"
            )

        print(
            f"\nRegla completada "
            f"({downloaded}/{needed})"
        )

    print("\n==============================")
    print("DESCARGA FINALIZADA")
    print(f"Total descargados: {downloads_today}")
    print("==============================")