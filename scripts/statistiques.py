import json


def charger_matchs():
    try:
        with open("matchs.json", "r", encoding="utf-8") as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        print("ERREUR : matchs.json est introuvable.")
        raise SystemExit(1)

    return data.get("response", [])


def preparer_match(match):
    return {
        "match_id": match["fixture"]["id"],
        "league_id": match["league"]["id"],
        "league": match["league"]["name"],
        "season": match["league"]["season"],
        "home_id": match["teams"]["home"]["id"],
        "home": match["teams"]["home"]["name"],
        "away_id": match["teams"]["away"]["id"],
        "away": match["teams"]["away"]["name"],
        "date": match["fixture"]["date"]
    }


def analyser():

    matchs = charger_matchs()

    print("=" * 70)
    print("FOOTZONE PRONO — PRÉPARATION DES DONNÉES")
    print("=" * 70)

    print("Matchs disponibles :", len(matchs))
    print()

    for match in matchs[:20]:

        infos = preparer_match(match)

        print(
            f"Match ID : {infos['match_id']} | "
            f"Ligue : {infos['league']} ({infos['league_id']}) | "
            f"Saison : {infos['season']}"
        )

        print(
            f"  {infos['home']} "
            f"(ID {infos['home_id']})"
            f"  VS  "
            f"{infos['away']} "
            f"(ID {infos['away_id']})"
        )

        print()

    print("=" * 70)
    print("FIN DE LA PRÉPARATION")
    print("=" * 70)


if __name__ == "__main__":
    analyser()
