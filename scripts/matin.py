import os
import json
import requests
from datetime import datetime, timezone

from quota import peut_faire_requete, ajouter_requete


API_KEY = os.environ["API_FOOTBALL_KEY"]

date_du_jour = datetime.now(timezone.utc).strftime("%Y-%m-%d")

print("=" * 70)
print("FOOTZONE PRONO — MATCHS DU JOUR")
print("=" * 70)
print("Date :", date_du_jour)
print()


# Vérification du quota avant l'appel API
if not peut_faire_requete():
    print("⚠️ QUOTA API INSUFFISANT")
    print("La récupération des matchs est arrêtée.")
    raise SystemExit(1)


url = "https://v3.football.api-sports.io/fixtures"

params = {
    "date": date_du_jour
}

headers = {
    "x-apisports-key": API_KEY,
    "Accept": "application/json"
}


response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=30
)


# Une requête API vient d'être effectuée
if not ajouter_requete():
    print("⚠️ Impossible d'enregistrer la requête.")
    raise SystemExit(1)


response.raise_for_status()

data = response.json()

if data.get("errors"):
    print("ERREURS API :", data["errors"])
    raise SystemExit(1)


matchs = data.get("response", [])


# Sauvegarde des données pour les autres modules
with open("matchs.json", "w", encoding="utf-8") as fichier:
    json.dump(
        data,
        fichier,
        ensure_ascii=False,
        indent=2
    )


print("Nombre de matchs trouvés :", len(matchs))
print("Données sauvegardées dans : matchs.json")
print()


for match in matchs:

    match_id = match["fixture"]["id"]
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]
    league = match["league"]["name"]
    heure = match["fixture"]["date"][11:16]
    statut = match["fixture"]["status"]["short"]

    print(
        f"ID: {match_id} | "
        f"{heure} | "
        f"{league} | "
        f"{home} - {away} | "
        f"{statut}"
    )


print()
print("=" * 70)
print("FIN DE LA RÉCUPÉRATION")
print("=" * 70)
