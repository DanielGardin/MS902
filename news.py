import pytz
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from sheet import get_worksheet

_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'}
_tz_brasil = pytz.timezone('America/Fortaleza')

class News:
    _last = None

    def __init__(self, news:pd.DataFrame, date):
        self.news = news
        self.date = date

    def __repr__(self):
        return repr(self.news)

    async def insert(self):
        worksheet = await get_worksheet()
        worksheet.append_rows(self.news.values.tolist(), value_input_option='USER_ENTERED')
        return 1


class RSS:
    def __init__(self, name:str, url:str, attrs:dict = {}):
        self.name = name
        self.url = url
        self.attrs = attrs

    def __repr__(self):
        return self.name

    async def scrap(self, date = None) -> News:
        news = pd.DataFrame()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=_headers) as response:
                    rss = await response.text()
                    soup = BeautifulSoup(rss, 'xml')
                    feed = soup.findAll('item')

                    if date is None:
                        for item in feed:
                            title = item.find('title').text
                            link = item.find('link').text
                            published = pd.to_datetime(item.find('pubDate').text)

                            try:
                                published = published.tz_convert(_tz_brasil)
                            except TypeError:
                                published = published.tz_localize(0).tz_convert(_tz_brasil)

                            new = {
                                'Fonte': self.name,
                                'Título': title,
                                'Link': link,
                                'Data': str(published)
                                }

                            news = news.append(new, ignore_index = True)

                    else:
                        for notice in feed:
                            published = pd.to_datetime(notice.find('pubDate').text)

                            try:
                                published = published.tz_convert(_tz_brasil)
                            except TypeError:
                                published = published.tz_localize(0).tz_convert(_tz_brasil)

                            if published <= date:
                                break

                            title = notice.find('title').text
                            link = notice.find('link').text

                            new = {
                                'Fonte': self.name,
                                'Título': title,
                                'Link': link,
                                'Data': str(published)
                                }

                            news = news.append(new, ignore_index = True)

                if news.empty:
                    return News(news, date)

                return News(news, pd.to_datetime(news['Data'].max()))
        except Exception as error:

            print(f"Erro com o scraping de {self.name}:{error}")
            return News(news, date)

    async def take_date(self):
        sheet = await get_worksheet()
        sheet = pd.DataFrame(sheet.get_all_records())
        try:
            limit = pd.to_datetime(sheet[sheet['Fonte'] == self.name]['Data'].max())

            if pd.isnull(limit):
                return None

            return limit

        except KeyError:
            return None
