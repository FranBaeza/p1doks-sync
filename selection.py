DOWNLOAD_PROFILES = {

    "DAY1": [

        {"series":"IMSA","class":"GT3","count":6},
        {"series":"GT Sprint","class":"GT3","count":8},
        {"series":"IMSA","class":"GTP","count":3},
        {"class":"LMP2","count":1},
        {"class":"PORSCHE_CUP","count":1},
        {"class":"GT4","count":3},
        {"class":"SF23","count":1},
        {"class":"SFL","count":1}

    ],

    "DAY2":[

        # luego lo rellenaremos

    ]

}

from selection_engine import build_download_queue


def build_profile(all_packs, profile_name):

    if profile_name == "DAY1":

        return build_download_queue(
            all_packs,
            DOWNLOAD_PROFILES["DAY1"]
        )

    elif profile_name == "DAY2":

        day1_queue = build_download_queue(
            all_packs,
            DOWNLOAD_PROFILES["DAY1"]
        )

        day1_ids = {

            pack["id"]

            for group in day1_queue

            for pack in group["packs"]

        }

        remaining = [

            pack

            for pack in all_packs

            if pack["id"] not in day1_ids

        ]

        return [

            {
                "rule": {
                    "count": len(remaining)
                },
                "packs": remaining
            }

        ]

    elif profile_name == "ALL":

        return [

            {
                "rule": {
                    "count": len(all_packs)
                },
                "packs": all_packs
            }

        ]

    raise Exception(f"Perfil desconocido: {profile_name}")