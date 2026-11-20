import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def kimai_origin(value):
    parts = urlsplit(value)
    if (parts.scheme != "https" or not parts.hostname or parts.username is not None
            or parts.path not in ("", "/") or "?" in value or "#" in value
            or "\\" in value or any(char.isspace() or ord(char) < 32 for char in value)):
        raise ValueError("KIMAI_URL doit être une origine HTTPS sans identifiants ni chemin.")
    if parts.port == 0:
        raise ValueError("Le port Kimai doit être positif.")
    return f"https://{parts.netloc}"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class Kimai:
    def __init__(self, expected_origin):
        self.origin = kimai_origin(os.environ.get("KIMAI_URL", ""))
        if self.origin != kimai_origin(expected_origin):
            raise ValueError("KIMAI_URL ne correspond pas à l'instance du profil choisi.")
        token = os.environ.get("KIMAI_TOKEN", "").strip()
        if not token:
            raise ValueError("KIMAI_TOKEN est absent de l'environnement.")
        self.headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        self.opener = build_opener(NoRedirect())

    def request(self, path, *, query=None, payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        url = f"{self.origin}/api/{path}" + (f"?{urlencode(query)}" if query else "")
        request = Request(url, data=data, headers={**self.headers, "Content-Type": "application/json"})
        try:
            with self.opener.open(request, timeout=20) as response:
                return json.load(response)
        except HTTPError as exc:
            raise ValueError(f"Kimai /api/{path} : HTTP {exc.code}.") from None
        except (URLError, TimeoutError, json.JSONDecodeError):
            raise ValueError(f"Kimai /api/{path} : réponse indisponible ou inattendue.") from None


def identifier(value):
    if isinstance(value, dict):
        value = value.get("id")
    if type(value) is not int or value <= 0:
        raise ValueError("Identifiant Kimai manquant ou invalide.")
    return value


def local_time(value, zone):
    if not isinstance(value, str):
        raise ValueError("Date locale Kimai invalide.")
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=zone)
    if result.fold or result.utcoffset() != result.replace(fold=1).utcoffset():
        raise ValueError("Horaire ambigu ou inexistant au changement d'heure.")
    return result


def proposed_entries(data, zone, increment_minutes):
    if not isinstance(data, list) or not data:
        raise ValueError("Le fichier doit contenir au moins une entrée confirmée.")
    records = []
    week = None
    for row in data:
        if not isinstance(row, dict) or row.keys() != {"begin", "end", "project", "activity"}:
            raise ValueError("Chaque entrée doit contenir uniquement begin, end, project et activity.")
        start, end = local_time(row["begin"], zone), local_time(row["end"], zone)
        if end <= start or end.date() != start.date() or (end - start).total_seconds() % (increment_minutes * 60):
            raise ValueError(f"Une entrée doit durer un multiple positif de {increment_minutes} min sur une seule date.")
        monday = start.date() - timedelta(days=start.weekday())
        if week not in (None, monday) or start.date() >= datetime.now(zone).date():
            raise ValueError("Limiter la saisie à une seule semaine et aux jours terminés.")
        week = monday
        records.append((start, end, identifier(row["project"]), identifier(row["activity"])))
    records.sort()
    if any(a[1] > b[0] for a, b in zip(records, records[1:])):
        raise ValueError("Les entrées proposées se chevauchent.")
    return records


def read_existing(api, user, proposed):
    begin = proposed[0][0].replace(hour=0, minute=0, second=0)
    end = proposed[-1][1].replace(hour=23, minute=59, second=59)
    query = {"user": user, "begin": (begin - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
             "end": end.strftime("%Y-%m-%dT%H:%M:%S"), "size": 50}
    existing = set()
    for page in range(1, 21):
        batch = api.request("timesheets", query={**query, "page": page})
        if not isinstance(batch, list):
            raise ValueError("Liste de feuilles de temps inattendue.")
        for row in batch:
            if identifier(row.get("user")) != user:
                raise ValueError("Kimai a renvoyé une entrée d'un autre compte.")
            start = datetime.fromisoformat(row["begin"])
            finish = datetime.fromisoformat(row["end"]) if row.get("end") else datetime.max.replace(tzinfo=timezone.utc)
            if start.utcoffset() is None or finish.utcoffset() is None:
                raise ValueError("Fuseau manquant dans une entrée Kimai.")
            existing.add((start.astimezone(timezone.utc), finish.astimezone(timezone.utc),
                          identifier(row["project"]), identifier(row["activity"])))
        if len(batch) < query["size"]:
            return existing
    raise ValueError("Pagination des feuilles de temps incomplète ; aucune saisie n'a été créée.")


def pending_entries(proposed, existing):
    pending = []
    for start, end, project, activity in proposed:
        exact = (start.astimezone(timezone.utc), end.astimezone(timezone.utc), project, activity)
        if exact in existing:
            continue
        if any(row[0] < exact[1] and row[1] > exact[0] for row in existing):
            raise ValueError(f"Chevauchement avec une saisie existante le {start:%d/%m/%Y} ; import arrêté.")
        pending.append((start, end, project, activity))
    return pending


def main():
    parser = argparse.ArgumentParser(description="Prévisualiser ou créer des saisies Kimai confirmées.")
    parser.add_argument("entries", type=Path)
    parser.add_argument("--timezone", required=True, help="Fuseau IANA du relevé")
    parser.add_argument("--increment-minutes", required=True, type=int, help="Pas de saisie en minutes")
    parser.add_argument("--instance", required=True, help="Origine HTTPS confirmée pour le profil choisi")
    parser.add_argument("--apply", action="store_true", help="Créer les seules entrées manquantes.")
    args = parser.parse_args()
    if args.increment_minutes < 1:
        parser.error("--increment-minutes doit être positif.")
    written = 0
    try:
        zone = ZoneInfo(args.timezone)
        proposed = proposed_entries(json.loads(args.entries.read_text()), zone, args.increment_minutes)
        api = Kimai(args.instance)
        me = api.request("users/me")
        user = identifier(me)
        if me.get("timezone") not in (None, zone.key):
            raise ValueError("Le fuseau du compte Kimai ne correspond pas au fuseau du relevé.")
        projects = {identifier(r) for r in api.request("projects") if r.get("visible") is True}
        activities = {identifier(r): r.get("project") for r in api.request("activities") if r.get("visible") is True}
        for _, _, project, activity in proposed:
            if project not in projects or activity not in activities:
                raise ValueError("Projet ou activité indisponible dans Kimai.")
            if activities[activity] is not None and identifier(activities[activity]) != project:
                raise ValueError("Cette activité n'appartient pas au projet indiqué.")
        pending = pending_entries(proposed, read_existing(api, user, proposed))
        print(f"{len(pending)} entrée(s) à créer ; {len(proposed) - len(pending)} déjà présentes.")
        if not args.apply:
            return
        for start, end, project, activity in pending:
            api.request("timesheets", payload={
                "begin": start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
                "project": project,
                "activity": activity,
            })
            written += 1
        remaining = pending_entries(proposed, read_existing(api, user, proposed))
        if remaining:
            raise ValueError("Certaines saisies ne sont pas visibles après création.")
        print(f"{written} entrée(s) créée(s) et vérifiée(s).")
    except ZoneInfoNotFoundError:
        parser.error("--timezone doit désigner un fuseau IANA disponible.")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Import arrêté ({written} création(s) confirmée(s) par l'API) : {exc}\n")


if __name__ == "__main__":
    main()
