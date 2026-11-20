# copilot-toolkit

Skills, agents et instructions personnels pour GitHub Copilot, à réutiliser d’un projet à l’autre.

## Skills disponibles

- [`analyse-issue`](skills/analyse-issue/) : analyse une issue GitHub dans le dépôt concerné.
- [`timesheet-orchestrator`](skills/timesheet-orchestrator/) : prépare le relevé de temps selon le profil choisi et coordonne les quatre skills suivants :
  - [`github-activities`](skills/github-activities/) : collecte les commits et vérifie leur rattachement aux tickets avec `gh`.
  - [`google-calendar-activities`](skills/google-calendar-activities/) : récupère les réunions via un connecteur autorisé ou `gws` et Python 3.9+.
  - [`time-aggregator`](skills/time-aggregator/) : calcule la grille hebdomadaire sans appeler de service.
  - [`fill-kimai`](skills/fill-kimai/) : prévisualise puis, sur autorisation explicite, importe les plages confirmées dans Kimai.

## Installer les skills

Avec une version récente de [GitHub CLI](https://cli.github.com/manual/gh_skill_install), connectez `gh` à un compte qui a accès au dépôt privé :

```sh
gh skill install delamotte-pierrick/copilot-toolkit --all --agent github-copilot --scope user
```

Cette commande installe les skills dans `~/.copilot/skills/`, pour tous vos projets. Pour limiter l’installation à un seul projet, lancez la commande depuis ce projet avec `--scope project`. Vérifiez la détection avec `/skills list` dans une nouvelle session Copilot CLI.

Pour tester des modifications qui ne sont pas encore sur GitHub, lancez la variante locale depuis la racine de `copilot-toolkit` :

```sh
gh skill install . --from-local --all --agent github-copilot --scope user
```

Si `gh` signale un conflit avec un skill copié à la main, sauvegardez ou déplacez ce dossier avant de relancer l’installation pour ne pas écraser vos modifications.

## Utiliser un profil de relevé

Après une installation personnelle, créez un profil par contexte de travail à partir du modèle livré avec le skill, sans cloner le dépôt :

```sh
mkdir -p "$HOME/.copilot/timesheet-profiles"
cp -i "$HOME/.copilot/skills/timesheet-orchestrator/profile.example.md" \
  "$HOME/.copilot/timesheet-profiles/mon-contexte.md"
```

Pour une installation au niveau du projet, le modèle est dans `.agents/skills/timesheet-orchestrator/` à la racine du projet.

Renseignez le fuseau, le périmètre GitHub, l’agenda, les horaires et les règles de saisie. Dans Copilot, demandez par exemple : « Utilise `timesheet-orchestrator` avec le profil `mon-contexte` pour préparer mon relevé du 5 au 9 janvier 2026. »

Pour changer d’entreprise, utilisez un autre profil et vérifiez les comptes connectés. Pour un import Kimai, sélectionnez séparément la paire `KIMAI_URL` et `KIMAI_TOKEN` associée au profil depuis votre gestionnaire de secrets. L’instance doit correspondre à celle du profil ; aucun jeton ne doit figurer dans le profil ou dans Git.

## Ajouter des ressources

| Fichier dans le kit | Pour tous vos projets (Copilot CLI) | Pour un seul projet |
| --- | --- | --- |
| `skills/<nom>/SKILL.md` | `~/.copilot/skills/<nom>/SKILL.md` | `.agents/skills/<nom>/SKILL.md` (avec `gh skill install`) |
| `agents/<nom>.agent.md` | `~/.copilot/agents/<nom>.agent.md` | `.github/agents/<nom>.agent.md` |
| `instructions/<nom>.instructions.md` | `~/.copilot/instructions/<nom>.instructions.md` | `.github/instructions/<nom>.instructions.md` |
| `copilot-instructions.md` | `~/.copilot/copilot-instructions.md` | `.github/copilot-instructions.md` |

Créez les dossiers `agents/` et `instructions/` au besoin. Pour un nouveau skill, ajoutez un en-tête YAML avec `name` et `description` et placez les scripts associés dans le même dossier. Ne versionnez ni secrets, ni paramètres locaux, ni journaux ou données de session.

[Référence des dossiers et fichiers de Copilot CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
