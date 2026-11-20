import argparse
import json
import subprocess
import sys
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def list_events(calendar_id, first, last, zone):
    params = {
        "calendarId": calendar_id,
        "timeMin": datetime.combine(first, time.min, zone).isoformat(),
        "timeMax": datetime.combine(last + timedelta(days=1), time.min, zone).isoformat(),
        "timeZone": zone.key,
        "singleEvents": True,
        "showDeleted": False,
        "showHiddenInvitations": True,
        "fields": (
            "nextPageToken,items(id,iCalUID,summary,status,eventType,transparency,"
            "start,end,attendees(self,responseStatus),organizer(self))"
        ),
    }
    events = []
    seen_tokens = set()
    while True:
        result = subprocess.run(
            ["gws", "calendar", "events", "list", "--params", json.dumps(params)],
            capture_output=True, text=True, timeout=60, check=False,
        )
        if result.returncode:
            raise RuntimeError(
                f"gws a échoué (code {result.returncode}). Vérifier l’autorisation "
                "Google Agenda et l’accès au calendrier sélectionné."
            )
        page = json.loads(result.stdout)
        if not isinstance(page, dict) or "error" in page or not isinstance(page.get("items", []), list):
            raise ValueError("Réponse Google Agenda inattendue.")
        events.extend(
            event for event in page.get("items", [])
            if not any(
                attendee.get("self") is True and attendee.get("responseStatus") == "declined"
                for attendee in event.get("attendees", [])
            )
        )
        token = page.get("nextPageToken")
        if not token:
            return events
        if not isinstance(token, str) or token in seen_tokens:
            raise ValueError("Jeton de pagination Google Agenda invalide ou répété.")
        seen_tokens.add(token)
        params["pageToken"] = token


def main():
    parser = argparse.ArgumentParser(description="Lire les événements Google Agenda, sans écriture.")
    parser.add_argument("--calendar", default="primary", help="Identifiant du calendrier (par défaut : primary)")
    parser.add_argument("--from", dest="first", required=True, type=date.fromisoformat)
    parser.add_argument("--to", dest="last", required=True, type=date.fromisoformat)
    parser.add_argument("--timezone", required=True, help="Fuseau IANA du relevé")
    args = parser.parse_args()
    if args.last < args.first:
        parser.error("--to doit être postérieur ou égal à --from")
    try:
        events = list_events(args.calendar, args.first, args.last, ZoneInfo(args.timezone))
    except ZoneInfoNotFoundError:
        parser.error("--timezone doit désigner un fuseau IANA disponible.")
    except FileNotFoundError:
        parser.exit(1, "Le client local gws n’est pas installé.\n")
    except (ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"Lecture Google Agenda impossible : {exc}\n")
    json.dump(events, sys.stdout, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
