import asyncio
from datetime import datetime
from pytz import timezone
import json
from news import RSS
import nest_asyncio
nest_asyncio.apply()

# Recebe as fontes utilizadas a partir de um 'fontes.json' e gera objetos
# do tipo RSS iteráveis
def get_sources() -> RSS:
    """
    Recebe as fontes utilizadas a partir do arquivo fontes.json e 
    gera objetos RSS iteráveis.
    """

    with open('fontes.json', encoding='utf-8') as sources:
        data = json.load(sources)

    print(f"Inicializando {len(data)} fontes:")

    for key, value in data.items():
        yield RSS(key, value['url'], value['attrs'])


async def searching_news(source:RSS) -> None:
    """
    Busca notícias da fonte 'source'  e as insere na tabela assincronamente 
    até que o programa seja encerrado.
    """

    print(f"Inicializando procura de notícias de {source}")
    time = await source.get_date()

    tz = timezone('America/Fortaleza')

    while True:
        table = await source.get_news(time)

        # Se alguma notícia for encontrada, classifique-as e insire-as
        if not table.news.empty:
            time = datetime.now(tz)
            await table.insert_news()
            print(f"{time}: Foram inseridas {len(table.news.index)} notícias.")

        # Aguarde até realizar a próxima busca
        await asyncio.sleep(300)


def main():
    loop = asyncio.get_event_loop()
    try:
        for source in get_sources():
            asyncio.ensure_future(searching_news(source))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()

if __name__ == '__main__':
    main()
