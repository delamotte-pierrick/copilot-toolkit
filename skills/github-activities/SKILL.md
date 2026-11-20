---
name: github-activities
description: Collecte en lecture seule les commits GitHub d'un compte dans un périmètre et une période définis, et les rattache à des tickets vérifiés.
---

# Collecter les activités GitHub

Entrées : dates inclusives, fuseau IANA, compte GitHub (par défaut le compte `gh` authentifié), organisation ou liste explicite de dépôts, et règle facultative de regroupement. Vérifier le compte avec `gh api user --jq '.login'`. Ne pas élargir le périmètre sans accord.

1. Rechercher ses PR de tous statuts, y compris celles ouvertes avant la période mais mises à jour depuis son début. Prévoir une marge de dates puis filtrer les commits en heure locale. Paginer les résultats et fractionner la recherche si elle atteint le plafond GitHub.
2. Lire les commits, liens d'issues, titre, description et branche des PR. Utiliser l'endpoint paginé `repos/OWNER/REPO/pulls/NUMBER/commits` si la vue PR est tronquée. Retenir les commits du compte dans la période, hors fusions, dédupliqués par SHA. Si plusieurs PR contiennent le même commit, préférer la PR de travail à une PR de livraison.
3. Rattacher chaque commit en confrontant les liens explicites, la référence dans le commit (par ex. `example-org/example-repo#42`), le titre et la branche. Vérifier que le lien désigne une issue pertinente. En cas d'ambiguïté non résolue, conserver la PR comme entrée distincte et expliquer la limite.
4. Si le profil demande un regroupement, suivre les parents avec `gh api repos/OWNER/REPO/issues/NUMBER/parent`, en limitant la remontée à la règle configurée et en évitant les cycles. Une mention croisée n'est pas une relation de parenté ; un accès refusé n'est pas une absence de parent. Sans règle, conserver le ticket direct.

Restituer pour chaque commit retenu : date locale, SHA, lien de PR, lien de ticket et parent confirmé s'ils sont établis. Signaler les dépôts inaccessibles, recherches tronquées ou rattachements ambigus. Ne pas calculer les durées à partir des commits.
