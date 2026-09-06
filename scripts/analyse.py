import os
import requests
from datetime import datetime

API_KEY = os.environ["API_FOOTBALL_KEY"]

DATE_DU_JOUR = datetime.utcnow().strftime("%Y-%m-%d")

URL = "https://v3.football.api-sports.io/fixtures"

HEADERS = {
    "x-apisports-key": API_KEY,
    "Accept": "application/json"
}


def recuperer_matchs():
    params = {
        "date": DATE_DU_JOUR
    }

    response = requests.get(
        URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        print("ERREURS API :", data["errors"])
        raise SystemExit(1)

    return data.get("response", [])


def afficher_resume(matchs):
    print("=" * 70)
    print("FOOTZONE PRONO — PRÉPARATION DE L'ANALYSE")
    print("=" * 70)
    print("Date :", DATE_DU_JOUR)
    print("Matchs récupérés :", len(matchs))
    print()

    for match in matchs:
        fixture = match["fixture"]
        teams = match["teams"]
        league = match["league"]

        match_id = fixture["id"]
        home = teams["home"]["name"]
        away = teams["away"]["name"]
        championnat = league["name"]

        print(
            f"ID: {match_id} | "
            f"{championnat} | "
            f"{home} - {away}"
        )

    print()
    print("=" * 70)
    print("FIN DE LA PRÉPARATION")
    print("=" * 70)


if __name__ == "__main__":
    matchs = recuperer_matchs()
    afficher_resume(matchs)
