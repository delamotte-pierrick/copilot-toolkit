---
name: google-calendar-activities
description: Collecte en lecture seule les intervalles de réunions professionnelles dans Google Agenda pour une période et un fuseau donnés.
---

# Collecter les activités Google Agenda

Entrées : dates inclusives, fuseau IANA, agenda choisi (`primary` par défaut), exclusions et exceptions confirmées. Utiliser un connecteur autorisé en lecture seule ou `gws` déjà configuré avec `calendar.events.readonly`. Ne rien installer ni connecter sans accord. N'utiliser un autre agenda que s'il est explicitement sélectionné.

Lister de minuit le premier jour à minuit le lendemain du dernier, en développant les récurrences et en suivant toutes les pages. Avec `gws` et Python 3.9+, lancer le script du dossier de ce skill, en remplaçant les valeurs d'exemple :

```sh
python3 /chemin/vers/google-calendar-activities/google_calendar.py \
  --from 2026-01-05 --to 2026-01-09 --timezone Etc/UTC
```

Ajouter `--calendar IDENTIFIANT` uniquement pour un autre agenda confirmé. Retenir les réunions professionnelles, y compris les invitations provisoires, sans réponse ou masquées. Écarter une invitation refusée uniquement si le refus est celui de l'utilisateur (`attendees[].self == true`). Exclure les événements annulés, journées entières, absences, événements personnels et blocs sans rapport avec une réunion. Demander une validation si la nature professionnelle d'un créneau est ambiguë.

Remettre à l'agrégateur les intervalles début/fin retenus et les limites de la collecte, sans titres ni participants. Ne pas déduire les absences de l'agenda. Ne pas traiter une erreur comme une liste vide, ni utiliser un horaire type de secours sans accord.
