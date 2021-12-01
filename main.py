import asyncio
import json
from news import RSS
import nest_asyncio
nest_asyncio.apply()

# Recebe as fontes utilizadas a partir de um 'fontes.json' e gera objetos
# do tipo RSS iteráveis
def get_sources() -> RSS:
    # Abrir e armazenar o JSON em um dicionário
    with open('fontes.json', encoding='utf-8') as sources:
        data = json.load(sources)

    print(f"Inicializando {len(data)} fontes:")

    for key, value in data.items():
        yield RSS(key, value['url'], value['attrs'])

# Corrotina que procura, classifica e insere notícias em repetição
async def searching_news(source:RSS):
    print(f"Inicializando procura de notícias de {source.name}")
    time = await source.get_date()

    while True:
        table = await source.get_news(time)

        # Se alguma notícia for encontrada, classifique e insira
        if not table.news.empty:
            time = table.date
            await table.insert_news()
            print(f"{time}: Foram inseridas {len(table.news.index)} notícias.")

        await asyncio.sleep(1)

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
