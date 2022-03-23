import requests
from pytz import timezone
import json
import re
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from sheet import get_worksheet, config

_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'}
_tz_brasil = timezone('America/Fortaleza')

with open('keywords.json', encoding='utf-8') as file:
    assets = json.load(file)

def standardize(content:str) -> str:
    """
    Padroniza o texto, retirando quaisquer caracteres que não sejam
    letras ou números.
    """

    text = content
    chars = [".",",",";",":","(", ")", "'",'"', "!", "?","/"]
    for char in chars:
        text = text.replace(char, '')

    return text.upper()


class News:
    _last = None

    def __init__(self, news:pd.DataFrame, date):
        self.news = news
        self.date = date

    def __repr__(self):
        return repr(self.news)

    async def insert_news(self):
        """"
        Insere notícias de um DataFrame para a planilha do Google configurada.
        """

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

    def get_tags(self, title:str, url:str) -> list[str]:
        """"
        Busca palavras-chave, definidas no arquivo keywords.json, no título ou corpo da notícia,
        este último realizando scrapping a partir do url da mesma.
        Retorna uma lista de possíveis tags para a notícia.
        """

        if config['classification'] == 'simple':
            try:
                assert bool(self.attrs)
                with requests.get(url, _headers) as response:
                    html = response.content
                    soup = BeautifulSoup(html, 'lxml')
                    content = soup.find('div', attrs=self.attrs)
                    text = standardize(content.get_text(separator=' ', strip=True))

            except:
                text = standardize(title)

            tags = []
            for asset in assets:
                if re.search(r'\b' + assets[asset][0] + r'\d ', text):
                    tags.append(asset)
                    break

                for keyword in assets[asset][1:]:
                    if re.search(r'\b'+keyword+r'\b', text):
                        tags.append(asset)
                        break

            return tags

        else:
            return ''


    async def get_news(self, date = None) -> News:
        """"
        Realiza scrapping no rss da fonte buscando por notícias recentes e que tenham
        tags de interesse.
        """

        news = pd.DataFrame()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=_headers) as response:
                    rss = await response.text()
                    soup = BeautifulSoup(rss, 'xml')
                    feed = soup.findAll('item')

                    if date is None:
                        for notice in feed:
                            title = notice.find('title').text
                            link = notice.find('link').text
                            published = pd.to_datetime(notice.find('pubDate').text)
                            tags = self.get_tags(title, link)

                            if not tags:
                                continue

                            try:
                                published = published.tz_convert(_tz_brasil)
                            except TypeError:
                                published = published.tz_localize(0).tz_convert(_tz_brasil)

                            new = {
                                'Fonte': self.name,
                                'Título': title,
                                'Link': link,
                                'Data': str(published),
                                'Tags': ', '.join(tags)
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
                            tags = self.get_tags(title, link)

                            if not tags:
                                continue

                            new = {
                                'Fonte': self.name,
                                'Título': title,
                                'Link': link,
                                'Data': str(published),
                                'Tags': ', '.join(tags)
                                }

                            news = news.append(new, ignore_index = True)

                if news.empty:
                    return News(news, date)

                return News(news, pd.to_datetime(news['Data'].max()))

        except Exception as error:
            print(f"Erro com o scraping de {self.name}:{error}. Tentando novamente...")
            return News(news, date)


    async def get_date(self):
        """
        Determina a data da última notícia inserida da fonte em questão. Retorna None
        se nenhuma for encontrada.
        """

        sheet = await get_worksheet()
        sheet = pd.DataFrame(sheet.get_all_records())
        try:
            limit = pd.to_datetime(sheet[sheet['Fonte'] == self.name]['Data'].max())

            if pd.isnull(limit):
                return None

            return limit

        except KeyError:
            return None
