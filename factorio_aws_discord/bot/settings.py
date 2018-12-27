import pathlib
import re
from datetime import timedelta

import yaml

time_units = {'w': timedelta(weeks=1),
              'd': timedelta(days=1),
              'h': timedelta(hours=1),
              'm': timedelta(minutes=1),
              's': timedelta(seconds=1)}


def parse_time(s: str) -> timedelta:
    matches = re.findall(r'(\d+)([wdhms])', s, re.IGNORECASE)
    total = timedelta(0)
    for match in matches:
        number, unit = match.groups()
        total += int(number) * time_units[unit]
    return total


class Settings:
    def __init__(self):
        path = pathlib.Path(__file__).resolve().parent.parent / 'settings.yaml'
        with path.open() as file:
            self._i = yaml.load(file)

    @property
    def bucket(self) -> str:
        return self._i['aws']['s3']['bucket']

    @property
    def region(self) -> str:
        return self._i['aws']['s3']['region']

    @property
    def bot_token(self) -> str:
        return self._i['discord']['client']['token']

    @property
    def root_member_names(self):
        return self._i['discord']['root']


settings = Settings()
