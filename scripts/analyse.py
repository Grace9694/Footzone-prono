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


# Compétitions que Footzone considère comme prioritaires
COMPETITIONS_PRIORITAIRES = {
    "UEFA Champions League",
    "UEFA Europa League",
    "UEFA Europa Conference League",
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "Ligue 1",
    "FA Cup",
    "Copa del Rey",
    "Coppa Italia",
    "DFB Pokal",
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


def calculer_score_initial(match):
    """
    Premier score de sélection.
    Ce score n'est PAS encore un pronostic.
    """

    score = 0

    league = match["league"]["name"]

    # Priorité aux grandes compétitions
    if league in COMPETITIONS_PRIORITAIRES:
        score += 40

    # Match avec deux équipes identifiées
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    if home and away:
        score += 20

    # Match ayant un horaire disponible
    if match["fixture"].get("date"):
        score += 10

    return score


def filtrer_matchs(matchs):
    selection = []

    for match in matchs:
        statut = match["fixture"]["status"]["short"]

        # On ignore les matchs déjà terminés
        if statut in {"FT", "AET", "PEN", "CANC", "PST", "ABD"}:
            continue

        score = calculer_score_initial(match)

        selection.append({
            "score": score,
            "match": match
        })

    # Classement du meilleur score au plus faible
    selection.sort(
        key=lambda element: element["score"],
        reverse=True
    )

    return selection


def afficher_selection(selection):
    print()
    print("=" * 70)
    print("FOOTZONE PRONO — PREMIÈRE SÉLECTION")
    print("=" * 70)

    print("Matchs candidats :", len(selection))
    print()

    for numero, element in enumerate(selection[:20], start=1):
        match = element["match"]

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        league = match["league"]["name"]
        heure = match["fixture"]["date"][11:16]

        print(
            f"{numero}. "
            f"[Score {element['score']}/70] "
            f"{heure} | "
            f"{league} | "
            f"{home} - {away}"
        )

    print()
    print("=" * 70)
    print("FIN DE LA PREMIÈRE SÉLECTION")
    print("=" * 70)


if __name__ == "__main__":
    matchs = recuperer_matchs()
    selection = filtrer_matchs(matchs)
    afficher_selection(selection)
