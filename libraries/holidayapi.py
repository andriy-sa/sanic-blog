import asyncio
import copy
import json
from datetime import datetime

import aiohttp


class v1:
    key = None
    params = {}

    def __init__(self, key, params):
        self.key = key
        self.params = params

    async def holidays(self, year):
        url = 'https://holidayapi.com/v1/holidays'

        if 'key' not in self.params:
            self.params['key'] = self.key
        params = copy.copy(self.params)
        params['year'] = year
        async with aiohttp.ClientSession() as session:
            text, status_code = await self.__fetch(session, url, params)

        data = json.loads(text)
        return data['holidays'] if status_code == 200 else []

    async def last_5_year_holidays(self):
        result = {}
        futures = []
        i = 6
        year = datetime.now().year

        loop = asyncio.get_event_loop()

        while i > 0:
            futures.append(loop.create_task(self.holidays(year)))
            year -= 1
            i -= 1
        for i, future in enumerate(asyncio.as_completed(futures)):
            holidays = await future
            if len(holidays):
                result.update(holidays)

        return result

    async def __fetch(self, session, url, params):
        async with session.get(url, params=params) as response:
            return await response.text(), response.status
