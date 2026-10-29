import json
from datetime import UTC, datetime


def marker_path(settings, label):
    return settings.out_dir / "sent" / f"{label}.json"


def already_sent(settings, label):
    return marker_path(settings, label).exists()


def mark_sent(settings, label, to):
    path = marker_path(settings, label)
    path.parent.mkdir(parents=True, exist_ok=True)
    sent = {
        "to": to,
        "at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    path.write_text(json.dumps(sent))
