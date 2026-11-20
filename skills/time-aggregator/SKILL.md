---
name: time-aggregator
description: Transforme les activités GitHub et les intervalles de réunion en relevé hebdomadaire, selon des horaires et règles de saisie fournis.
---

# Agréger le temps

Entrées : période, fuseau IANA, minutes de base par jour ouvré, congés et absences confirmés, jours fériés, rattrapages confirmés, pas de saisie, libellés, tickets avec leurs regroupements et intervalles de réunion. Ne pas appeler de service. Calculer en minutes avant d'arrondir.

- **Cible** : additionner les minutes de base des jours de la période. Retirer les jours fériés chômés et les congés confirmés, sans déduire deux fois un même intervalle. Une absence avec rattrapage ne réduit pas la cible. Une demi-journée vaut la moitié du temps de base du jour, sauf durée confirmée différente. Si son créneau est inconnu, signaler tout chevauchement à valider.
- **Réunions** : découper aux frontières des jours du fuseau, retirer les créneaux chômés ou d'absence et prendre l'union des intervalles. Signaler si le total dépasse le temps disponible, sans créer de durée négative.
- **Tickets** : répartir à parts égales le temps de base restant entre les tickets distincts actifs ce jour-là ; départager les minutes restantes dans un ordre stable, par ex. par identifiant de ticket. En l'absence de ticket, laisser ce solde à répartir. Si une source est incomplète, qualifier le calcul de provisoire et ne pas traiter les données manquantes comme des zéros vérifiés.
- **Rattrapage** : ajouter seulement le temps effectivement rattrapé et confirmé aux dates et activités connues. Afficher le solde restant à récupérer séparément du temps à répartir. Les congés confirmés peuvent figurer sur une ligne distincte, hors total travaillé.
- **Arrondi** : regrouper d'abord par catégorie ou parent selon le profil. Pour chaque semaine, arrondir au pas choisi selon la méthode des plus grands restes ; départager les restes à égalité dans un ordre stable, préserver les cases déjà au pas et ne rien ajouter à un jour à zéro. Signaler tout écart avec les minutes exactes et conserver les durées exactes si l'arrondi ne respecte pas les contraintes.

Restituer une grille par semaine (`Projet | Activité | Lun. | Mar. | Mer. | Jeu. | Ven. | Sam. | Dim. | Durée`, total travaillé, `H:MM`, `0:00` pour une case vide, `—` hors période) et le détail exact par parent et par ticket : lien, premier et dernier commit, jours d'activité et durée avant arrondi. Vérifier les totaux, les absences, les multiples du pas et l'absence de doubles comptes. Le relevé estime la répartition à partir d'indices d'activité ; ce n'est pas une mesure du temps réel.
