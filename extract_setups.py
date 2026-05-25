import json
import zipfile
import shutil
from pathlib import Path

# =========================
# CONFIG
# =========================

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open("car_mapping.json", "r", encoding="utf-8") as f:
    car_mapping = json.load(f)

with open("all_packs.json", "r", encoding="utf-8") as f:
    all_packs = json.load(f)

downloads_path = Path("downloads")

iracing_base = Path(config["iracing_setups_path"])

# =========================
# HELPERS
# =========================

def normalize_folder(text):

    text = text.lower()

    replacements = {
        " ": "",
        "/": "-",
        "\\": "-",
        ":": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

# =========================
# PROCESAR ZIPS
# =========================

zip_files = list(downloads_path.glob("*.zip"))

print(f"\nProcesando {len(zip_files)} ZIPs...\n")

for zip_file in zip_files:

    print(f"\nZIP: {zip_file.name}")

    matching_pack = None

    # Buscar datapack asociado
    for pack in all_packs:

        if (
            pack["Series"] in zip_file.name
            and pack["Car"] in zip_file.name
        ):
            matching_pack = pack
            break

    if not matching_pack:
        print("  -> No se encontró datapack")
        continue

    car_name = matching_pack["Car"]

    iracing_folder = car_mapping.get(car_name)

    if not iracing_folder:
        print(f"  -> Mapping faltante: {car_name}")
        continue

    # =========================
    # CONSTRUIR RUTA FINAL
    # =========================

    season_folder = (
        f"{matching_pack['Year']}-"
        f"S{matching_pack['Season']}"
    )

    series_folder = normalize_folder(
        matching_pack["Series"]
    )

    track_folder = matching_pack["Track"]

    target_folder = (
        iracing_base
        / iracing_folder
        / "Garage 61 - ZRT MOMO"
        / "P1DOKS"
        / season_folder
        / series_folder
        / track_folder
    )

    target_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"  -> Destino:")
    print(f"     {target_folder}")

    # =========================
    # EXTRAER .STO
    # =========================

    with zipfile.ZipFile(zip_file, "r") as zip_ref:

        for member in zip_ref.namelist():

            if not member.endswith(".sto"):
                continue

            filename = Path(member).name

            final_path = target_folder / filename

            print(f"     -> Copiando {filename}")

            with zip_ref.open(member) as source:
                with open(final_path, "wb") as target:
                    shutil.copyfileobj(source, target)

print("\nProceso completado.")