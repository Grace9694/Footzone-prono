import json
import requests
import os

API_KEY = os.environ["API_FOOTBALL_KEY"]

URL = "https://v3.football.api-sports.io/teams/statistics"

HEADERS = {
    "x-apisports-key": API_KEY,
    "Accept": "application/json"
}


def charger_candidats():
    """Charge les candidats issus de l'analyse initiale."""

    try:
        with open("matchs.json", "r", encoding="utf-8") as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        print("ERREUR : matchs.json est introuvable.")
        raise SystemExit(1)

    return data.get("response", [])


def recuperer_statistiques(team_id, league_id, saison):
    """Récupère les statistiques d'une équipe."""

    params = {
        "team": team_id,
        "league": league_id,
        "season": saison
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
        print("ERREUR API :", data["errors"])
        return None

    return data.get("response")


def analyser():

    matchs = charger_candidats()

    print("=" * 70)
    print("FOOTZONE PRONO — MODULE STATISTIQUES")
    print("=" * 70)

    print("Matchs disponibles :", len(matchs))
    print()

    # Pour l'instant, on vérifie simplement que les données
    # nécessaires sont présentes.
    for match in matchs[:20]:

        home = match["teams"]["home"]
        away = match["teams"]["away"]

        print(
            f"{home['name']} "
            f"(ID {home['id']}) vs "
            f"{away['name']} "
            f"(ID {away['id']})"
        )

    print()
    print("=" * 70)
    print("FIN DU MODULE STATISTIQUES")
    print("=" * 70)


if __name__ == "__main__":
    analyser()
