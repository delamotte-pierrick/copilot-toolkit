# Profil de relevé — exemple

Copier ce modèle dans `~/.copilot/timesheet-profiles/<profil>.md` et remplacer les valeurs d'exemple avant usage. Utiliser un fichier par contexte de travail. Ne pas y enregistrer de jetons, d'événements ni de relevés.

| Paramètre | Valeur d'exemple |
| --- | --- |
| Fuseau IANA | `Etc/UTC` |
| Périmètre GitHub | Liste de dépôts `example-org/example-repo` ou organisation `example-org` |
| Compte GitHub | Compte `gh` authentifié ; le vérifier avant de collecter |
| Regroupement des tickets | Ticket direct, ou remonter jusqu'à un parent dans un dépôt explicitement indiqué |
| Tickets sans parent confirmé | Conserver le ticket direct, ou regrouper sous un libellé explicitement choisi |
| Google Agenda | `primary` du compte autorisé, ou identifiant explicitement choisi ; préciser les exclusions métier utiles |
| Temps de base par jour ouvré | Lun.–ven. : 480 min par jour ; sam.–dim. : 0 |
| Pas de saisie | 15 min ; choisir 1 min pour ne pas arrondir |
| Libellés du relevé | Développement, Réunions, Congés, À répartir |
| Kimai (facultatif) | Origine HTTPS `https://kimai.example.com` ; correspondances projet/activité par identifiants, à compléter |

Confirmer les jours fériés, absences, rattrapages et exceptions pour chaque période. Pour changer de contexte, sélectionner un autre profil et vérifier les comptes GitHub, Google et Kimai actifs ; le profil ne change pas les comptes connectés.
