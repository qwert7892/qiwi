import requests
import json
from datetime import datetime as dt
from datetime import timedelta as td
import random


class Bill:
    def __init__(self, money: (float, int), currency: str = 'RUB'):
        self.id = random.choice(range(1000000))
        t = dt.now() + td(hours=1)
        self.time = str(t)[:-7].replace(' ', 'T')
        self.money = money
        self.currency = currency

        headers = {
            'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InJ5MG51Zy0wMCIsInVzZXJfaWQiOiI3OTk2OTI1NzA1NCIsInNlY3JldCI6ImUyM2NkYTE3OTM3ZmY0MDNlMzc3MjhmYjkyMGQ4ZDE3M2IyNzQ2YjgwYjYyYWE5Mzk3MmI5ZTRiZWFjZmJhNjMifX0=',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        params = {'amount': {'value': self.money,
                             'currency': self.currency,
                             },
                  'comment': 'Text comment',
                  'expirationDateTime': f'{self.time}+03:00',
                  'customer': {},
                  'customFields': {},
                  }

        params = json.dumps(params)

        self.result = requests.put(f'https://api.qiwi.com/partner/bill/v1/bills/{self.id}',
                                   headers=headers,
                                   data=params,
                                   ).json()

        self.url = self.result.get('payUrl')

    def check_status(self):
        headers = {
            'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InJ5MG51Zy0wMCIsInVzZXJfaWQiOiI3OTk2OTI1NzA1NCIsInNlY3JldCI6ImUyM2NkYTE3OTM3ZmY0MDNlMzc3MjhmYjkyMGQ4ZDE3M2IyNzQ2YjgwYjYyYWE5Mzk3MmI5ZTRiZWFjZmJhNjMifX0=',
            'Accept': 'application/json'
        }

        res = requests.get(f'https://api.qiwi.com/partner/bill/v1/bills/{self.id}', headers=headers)
        return res.json().get('status')
