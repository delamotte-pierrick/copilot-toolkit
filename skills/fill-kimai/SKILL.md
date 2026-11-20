---
name: fill-kimai
description: Prévisualise un import Kimai à partir de plages et correspondances confirmées, et ne crée des entrées que sur autorisation explicite.
---

# Prévisualiser ou importer dans Kimai

Entrées : origine HTTPS Kimai du profil choisi, fuseau IANA, pas de saisie, et plages confirmées avec leurs identifiants de projet et d'activité. Ne pas produire le relevé ni déduire les heures à partir de durées agrégées. Si l'utilisateur veut produire le relevé complet, utiliser `timesheet-orchestrator`.

1. Vérifier la correspondance des libellés aux identifiants. Utiliser uniquement des plages confirmées ou une convention approuvée par l'utilisateur. Exclure les temps à répartir, rattrapages non confirmés et données brutes d'agenda. Arrêter si les correspondances ou créneaux manquent.
2. Préparer un JSON pour une seule semaine de jours terminés : une liste d'objets contenant seulement `begin`, `end` (dates et heures locales `YYYY-MM-DDTHH:MM:SS`), `project` et `activity` (identifiants numériques).
3. Configurer `KIMAI_URL` et `KIMAI_TOKEN` dans l'environnement du processus via un gestionnaire de secrets. En changeant de profil, sélectionner la paire associée sans afficher le jeton ni le demander dans le chat. Passer l'origine confirmée du profil séparément au script. Le lancer d'abord en prévisualisation :

   ```sh
   python3 /chemin/vers/fill-kimai/kimai.py /chemin/vers/saisies.json \
     --timezone Etc/UTC --increment-minutes 15 --instance https://kimai.example.com
   ```

4. Communiquer le résultat de la prévisualisation. Le script ignore les entrées identiques et bloque les chevauchements. Ajouter `--apply` uniquement après autorisation explicite pour cette instance et ces entrées. Ne pas lancer deux imports simultanément ; après un import partiel ou une réponse incertaine, relire les entrées avant de réessayer.
