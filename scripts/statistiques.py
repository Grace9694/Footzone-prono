import json
import os
import requests

from quota import peut_faire_requete, ajouter_requete


API_KEY = os.environ["API_FOOTBALL_KEY"]

URL = "https://v3.football.api-sports.io/fixtures"

HEADERS = {
    "x-apisports-key": API_KEY,
    "Accept": "application/json"
}


def charger_candidats():

    try:
        with open("candidats.json", "r", encoding="utf-8") as fichier:
            return json.load(fichier)

    except FileNotFoundError:
        print("ERREUR : candidats.json est introuvable.")
        raise SystemExit(1)


def recuperer_forme_equipe(team_id):

    # Vérification du quota avant la requête
    if not peut_faire_requete():
        print("⚠️ QUOTA API INSUFFISANT")
        return None

    params = {
        "team": team_id,
        "last": 5
    }

    response = requests.get(
        URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    # Une requête vient d'être effectuée
    if not ajouter_requete():
        print("⚠️ Impossible d'enregistrer la requête.")
        return None

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        print("ERREURS API :", data["errors"])
        return None

    return data.get("response", [])


def calculer_forme(matchs, team_id):

    victoires = 0
    nuls = 0
    defaites = 0
    buts_marques = 0
    buts_encaisses = 0

    matchs_termines = 0

    for match in matchs:

        statut = match["fixture"]["status"]["short"]

        if statut not in {"FT", "AET", "PEN"}:
            continue

        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        home_goals = match["goals"]["home"]
        away_goals = match["goals"]["away"]

        if home_goals is None or away_goals is None:
            continue

        matchs_termines += 1

        if team_id == home_id:

            buts_marques += home_goals
            buts_encaisses += away_goals

            if home_goals > away_goals:
                victoires += 1
            elif home_goals == away_goals:
                nuls += 1
            else:
                defaites += 1

        elif team_id == away_id:

            buts_marques += away_goals
            buts_encaisses += home_goals

            if away_goals > home_goals:
                victoires += 1
            elif away_goals == home_goals:
                nuls += 1
            else:
                defaites += 1

    return {
        "matchs": matchs_termines,
        "victoires": victoires,
        "nuls": nuls,
        "defaites": defaites,
        "buts_marques": buts_marques,
        "buts_encaisses": buts_encaisses
    }


def analyser():

    candidats = charger_candidats()

    print("=" * 70)
    print("FOOTZONE PRONO — FORME RÉCENTE")
    print("=" * 70)

    print("Candidats à analyser :", len(candidats))
    print()

    # Cache pour éviter de demander plusieurs fois
    # les mêmes statistiques
    formes = {}

    for element in candidats:

        match = element["match"]

        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        print(f"Analyse : {home} - {away}")

        # Équipe à domicile
        if home_id not in formes:

            matchs_home = recuperer_forme_equipe(home_id)

            if matchs_home is not None:
                formes[home_id] = calculer_forme(
                    matchs_home,
                    home_id
                )

        # Équipe à l'extérieur
        if away_id not in formes:

            matchs_away = recuperer_forme_equipe(away_id)

            if matchs_away is not None:
                formes[away_id] = calculer_forme(
                    matchs_away,
                    away_id
                )

    # Sauvegarde
    with open("formes.json", "w", encoding="utf-8") as fichier:

        json.dump(
            formes,
            fichier,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("Données sauvegardées dans : formes.json")
    print()

    # Affichage
    for element in candidats:

        match = element["match"]

        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        forme_home = formes.get(home_id)
        forme_away = formes.get(away_id)

        print(f"{home} :")

        if forme_home:
            print(
                f"  {forme_home['victoires']} V | "
                f"{forme_home['nuls']} N | "
                f"{forme_home['defaites']} D | "
                f"{forme_home['buts_marques']} buts marqués | "
                f"{forme_home['buts_encaisses']} encaissés"
            )

        print(f"{away} :")

        if forme_away:
            print(
                f"  {forme_away['victoires']} V | "
                f"{forme_away['nuls']} N | "
                f"{forme_away['defaites']} D | "
                f"{forme_away['buts_marques']} buts marqués | "
                f"{forme_away['buts_encaisses']} encaissés"
            )

        print()

    print("=" * 70)
    print("FIN DE L'ANALYSE DE FORME")
    print("=" * 70)


if __name__ == "__main__":
    analyser()
