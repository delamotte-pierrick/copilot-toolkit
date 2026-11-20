---
name: analyse-issue
description: Analyse une issue GitHub et le code du dépôt concerné pour décrire l'existant, répondre aux questions vérifiables et proposer une solution technique. Utiliser lorsqu'une issue doit être analysée, quel que soit le dépôt.
---

# Analyse d'issue GitHub

Pour toute issue GitHub fournie :

- Détermine le dépôt à partir de l'URL de l'issue ou du dépôt explicitement indiqué. Si l'utilisateur ne donne qu'un numéro et que le dépôt ne peut pas être déterminé sans ambiguïté à partir du contexte courant, demande lequel.
- Utilise `gh` en lecture seule pour récupérer l'issue et ses commentaires. Si elle a une issue parente, récupère aussi celle-ci pour le contexte. N'effectue aucune modification sur GitHub.
- Analyse le code du dépôt correspondant à l'issue, ou du dépôt explicitement demandé. Ne suppose pas qu'il s'agit du dépôt courant. Si le code n'est pas accessible, indique cette limite et n'invente pas de comportement ou de fichiers impactés.
- Appuie-toi uniquement sur les éléments vérifiables de l'issue, de ses commentaires, de son parent, du code pertinent et des précisions de l'utilisateur. N'invente aucun fait.
- Si l'utilisateur fournit un commentaire précis en complément de l'issue, considère les informations qu'il contient comme une source de vérité pour l'analyse, même si elles ne figurent pas dans l'issue ou le code. N'en déduis pas d'informations supplémentaires qui n'y sont pas indiquées.
- Utilise l'issue parente et les commentaires comme contexte, mais limite l'analyse et la solution au périmètre de l'issue fournie.
- Pour toute analyse du code, identifie les fichiers impactés à partir du code existant et explique brièvement pourquoi chacun est concerné. Ne présente pas une hypothèse comme un fait établi.
- Dans « Questions et Réponses », distingue les questions présentes dans l'issue de celles qui restent ouvertes après analyse. Ne donne une réponse que si elle est étayée par l'issue, ses commentaires, son parent ou le code. Indique explicitement quand aucune question ne reste ouverte.

Réponds en français et strictement avec ces trois sections, dans cet ordre, sans introduction ni conclusion :

## 1. Existant

Décris uniquement le comportement ou l'implémentation actuelle, étayés par le code ou les éléments vérifiables de l'issue.

## 2. Questions et Réponses

Reporte les questions posées dans l'issue et les réponses vérifiables, puis les éventuelles questions ouvertes.

## 3. Solution technique (fichiers impactés + objectif)

Décris la solution proposée dans le périmètre de l'issue et liste les fichiers impactés avec l'objectif de chaque changement. Si aucun fichier ne peut être confirmé à partir du code accessible, indique-le explicitement.
