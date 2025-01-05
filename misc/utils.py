import os
import re
import unicodedata
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo(os.getenv("TZ"))


class Colors:
    _colorize = lambda color, *args: f"\033[{color}m{' '.join(map(str, args))}\033[0m"

    green = lambda *args: Colors._colorize(32, *args)
    red = lambda *args: Colors._colorize(31, *args)
    yellow = lambda *args: Colors._colorize(33, *args)


def slugify(text, separator="-"):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", separator, text).strip(separator)

    return text


def is_from_last_24h(iso_datetime_str):
    dt_obj = datetime.strptime(iso_datetime_str, "%Y-%m-%d %H:%M").replace(tzinfo=TZ)
    cutoff = datetime.now(TZ) - timedelta(hours=24)

    return dt_obj > cutoff


def now():
    return datetime.now(TZ)
