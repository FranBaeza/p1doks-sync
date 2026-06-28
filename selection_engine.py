from classes import CAR_CLASSES


def build_download_queue(all_packs, profile):

    download_groups = []
    selected_ids = set()

    for rule in profile:

        # Packs candidatos
        candidates = all_packs

        # ===========================
        # Filtrar por serie
        # ===========================

        if "series" in rule:
            candidates = [
                p for p in candidates
                if p["Series"] == rule["series"]
            ]

        # ===========================
        # Filtrar por clase
        # ===========================

        if "class" in rule:

            allowed_aliases = CAR_CLASSES[rule["class"]]

            candidates = [

                p for p in candidates

                if any(

                    alias.lower() in p["Car"].lower()

                    for alias in allowed_aliases

                )

            ]

        # ===========================
        # Coger coches únicos
        # ===========================
        group_packs = []

        selected_cars = set()

        for pack in candidates:

            car = pack["Car"]

            if car in selected_cars:
                continue

            if pack["id"] in selected_ids:
                continue

            selected_cars.add(car)
            selected_ids.add(pack["id"])

            group_packs.append(pack)

        download_groups.append({
        "rule": rule,
        "packs": group_packs
        })

    print("\n=== SETUPS A DESCARGAR ===")

    for group in download_groups:

        print(f"\n{group['rule']}")

        for pack in group["packs"]:

            print(
                f"   {pack['Series']} | "
                f"{pack['Car']} | "
                f"{pack['lap_time_formatted']}"
            )

    return download_groups