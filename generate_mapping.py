import json
from pathlib import Path
from rapidfuzz import process, fuzz

# =========================
# CONFIG
# =========================

IRACING_SETUPS = Path(
    r"C:\Users\Fran\Documents\iRacing\setups"
)

# =========================
# CARGAR DATAPACKS
# =========================

with open("all_packs.json", "r", encoding="utf-8") as f:
    all_packs = json.load(f)

# =========================
# OBTENER COCHES ÚNICOS
# =========================

cars = sorted(set(pack["Car"] for pack in all_packs))

# =========================
# CARPETAS IRACING
# =========================

folders = [
    folder.name
    for folder in IRACING_SETUPS.iterdir()
    if folder.is_dir()
]

# =========================
# NORMALIZADOR
# =========================

def normalize(text):

    text = text.lower()

    replacements = {
        " ": "",
        "-": "",
        "_": "",
        "gt3": "gt3",
        "evo": "evo",
        "porsche911": "porsche",
        "mercedesamg": "mercedes",
        "bmwm4": "bmw",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

# =========================
# GENERAR MATCHES
# =========================

mapping = {}

print("\n=== SUGERENCIAS ===\n")

for car in cars:

    normalized_car = normalize(car)

    result = process.extractOne(
        normalized_car,
        folders,
        scorer=fuzz.ratio
    )

    if result:

        best_match, score, _ = result

        print(f"{car}")
        print(f"  -> {best_match} ({score:.1f})")

        mapping[car] = best_match

# =========================
# GUARDAR JSON
# =========================

with open("car_mapping.json", "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=4)

print("\ncar_mapping.json generado")