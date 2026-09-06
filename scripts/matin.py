import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

# Clé API stockée dans GitHub Secrets
API_KEY = os.environ["API_FOOTBALL_KEY"]

# Heure du Bénin
TZ = ZoneInfo("Africa/Porto-Novo")
maintenant = datetime.now(TZ)
date_du_jour = maintenant.strftime("%Y-%m-%d")

print("=" * 60)
print("FOOTZONE PRONO — MATCHS DU JOUR")
print("=" * 60)
print("Date du Bénin :", date_du_jour)
print()

url = "https://v3.football.api-sports.io/fixtures"

params = {
    "date": date_du_jour,
    "timezone": "Africa/Porto-Novo"
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

response.raise_for_status()
data = response.json()

# Vérification des erreurs API
if data.get("errors"):
    print("ERREURS API :", data["errors"])
    raise SystemExit(1)

matchs = data.get("response", [])

print("Nombre de matchs trouvés :", len(matchs))
print()

# Affichage des matchs
for match in matchs:
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]
    league = match["league"]["name"]
    heure = match["fixture"]["date"][11:16]
    statut = match["fixture"]["status"]["short"]

    print(f"{heure} | {league} | {home} - {away} | {statut}")

print()
print("=" * 60)
print("FIN DE LA RÉCUPÉRATION")
print("=" * 60)
