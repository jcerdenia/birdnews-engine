from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class Clock:
    def __init__(self, tz):
        self.tz = ZoneInfo(tz)

    def now(self):
        return datetime.now(self.tz)

    def is_from_last_24h(self, iso_datetime_str):
        format = "%Y-%m-%d %H:%M"
        dt_obj = datetime.strptime(iso_datetime_str, format).replace(tzinfo=self.tz)
        cutoff = datetime.now(self.tz) - timedelta(hours=24)

        return dt_obj > cutoff

    def is_start_of_week(self):
        return self.now().weekday() == 0 and self.now().hour == 0

    @classmethod
    def from_config(cls, config):
        return cls(config.TZ)
