import json


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


def charger_matchs():
    """Charge les matchs récupérés par matin.py."""

    try:
        with open("matchs.json", "r", encoding="utf-8") as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        print("ERREUR : le fichier matchs.json est introuvable.")
        raise SystemExit(1)

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

    # Deux équipes correctement identifiées
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    if home and away:
        score += 20

    # Horaire disponible
    if match["fixture"].get("date"):
        score += 10

    return score


def filtrer_matchs(matchs):
    selection = []

    for match in matchs:

        statut = match["fixture"]["status"]["short"]

        # On ignore les matchs déjà terminés,
        # annulés, reportés ou abandonnés
        if statut in {"FT", "AET", "PEN", "CANC", "PST", "ABD"}:
            continue

        score = calculer_score_initial(match)

        selection.append({
            "score": score,
            "match": match
        })

    # Meilleur score en premier
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

    matchs = charger_matchs()

    selection = filtrer_matchs(matchs)

    afficher_selection(selection)
