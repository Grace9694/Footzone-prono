import json
import os
from datetime import datetime, timezone


QUOTA_JOURNALIER = 100
FICHIER_QUOTA = "quota.json"


def charger_quota():
    aujourd_hui = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not os.path.exists(FICHIER_QUOTA):
        return {
            "date": aujourd_hui,
            "requêtes": 0
        }

    with open(FICHIER_QUOTA, "r", encoding="utf-8") as fichier:
        quota = json.load(fichier)

    # Nouveau jour : on recommence le compteur
    if quota.get("date") != aujourd_hui:
        return {
            "date": aujourd_hui,
            "requêtes": 0
        }

    return quota


def enregistrer_quota(quota):
    with open(FICHIER_QUOTA, "w", encoding="utf-8") as fichier:
        json.dump(quota, fichier, ensure_ascii=False, indent=2)


def peut_faire_requete(nombre=1):
    quota = charger_quota()

    return quota["requêtes"] + nombre <= QUOTA_JOURNALIER


def ajouter_requete(nombre=1):
    quota = charger_quota()

    if quota["requêtes"] + nombre > QUOTA_JOURNALIER:
        print("⚠️ QUOTA API ATTEINT")
        return False

    quota["requêtes"] += nombre

    enregistrer_quota(quota)

    print(
        f"Requêtes comptabilisées : "
        f"{quota['requêtes']}/{QUOTA_JOURNALIER}"
    )

    return True


def afficher_quota():
    quota = charger_quota()

    restantes = QUOTA_JOURNALIER - quota["requêtes"]

    print(
        f"Quota utilisé : "
        f"{quota['requêtes']}/{QUOTA_JOURNALIER}"
    )

    print(
        f"Quota restant : "
        f"{restantes}"
    )


if __name__ == "__main__":
    print("=" * 50)
    print("FOOTZONE PRONO — CONTRÔLE DU QUOTA")
    print("=" * 50)

    afficher_quota()

    print("=" * 50)
