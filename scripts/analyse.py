import json


# Compétitions prioritaires
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


def charger_matchs():
    """Charge les matchs récupérés par matin.py."""

    try:
        with open("matchs.json", "r", encoding="utf-8") as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        print("ERREUR : matchs.json est introuvable.")
        raise SystemExit(1)

    if data.get("errors"):
        print("ERREURS API :", data["errors"])
        raise SystemExit(1)

    return data.get("response", [])


def calculer_score_initial(match):
    """
    Score de présélection.
    Ce n'est PAS encore le score sportif final.
    """

    score = 0

    league = match["league"]["name"]

    # Grande compétition
    if league in COMPETITIONS_PRIORITAIRES:
        score += 40

    # Deux équipes identifiées
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    if home and away:
        score += 20

    # Date/heure disponible
    if match["fixture"].get("date"):
        score += 10

    return score


def filtrer_matchs(matchs):
    candidats = []

    for match in matchs:

        statut = match["fixture"]["status"]["short"]

        # On ignore les matchs non exploitables
        if statut in {"FT", "AET", "PEN", "CANC", "PST", "ABD"}:
            continue

        score = calculer_score_initial(match)

        candidats.append({
            "score_initial": score,
            "match": match
        })

    # Meilleurs candidats en premier
    candidats.sort(
        key=lambda element: element["score_initial"],
        reverse=True
    )

    # Maximum 20 candidats pour l'analyse approfondie
    return candidats[:20]


def sauvegarder_candidats(candidats):

    with open("candidats.json", "w", encoding="utf-8") as fichier:
        json.dump(
            candidats,
            fichier,
            ensure_ascii=False,
            indent=2
        )

    print("Candidats sauvegardés dans : candidats.json")


def afficher_selection(candidats):

    print()
    print("=" * 70)
    print("FOOTZONE PRONO — CANDIDATS À ANALYSER")
    print("=" * 70)

    print("Nombre de candidats :", len(candidats))
    print()

    for numero, element in enumerate(candidats, start=1):

        match = element["match"]

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        league = match["league"]["name"]
        heure = match["fixture"]["date"][11:16]

        print(
            f"{numero}. "
            f"[Score initial {element['score_initial']}/70] "
            f"{heure} | "
            f"{league} | "
            f"{home} - {away}"
        )

    print()
    print("=" * 70)


if __name__ == "__main__":

    matchs = charger_matchs()

    candidats = filtrer_matchs(matchs)

    sauvegarder_candidats(candidats)

    afficher_selection(candidats)
