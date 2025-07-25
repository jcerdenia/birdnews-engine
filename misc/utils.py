import re
import unicodedata
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


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


def is_from_last_24h(iso_datetime_str, tz):
    tzinfo = ZoneInfo(tz)
    format = "%Y-%m-%d %H:%M"

    dt_obj = datetime.strptime(iso_datetime_str, format).replace(tzinfo=tzinfo)
    cutoff = datetime.now(tzinfo) - timedelta(hours=24)

    return dt_obj > cutoff


def now(tz):
    return datetime.now(ZoneInfo(tz))
