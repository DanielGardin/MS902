import json
from google.oauth2 import service_account
import gspread as gs

async def get_worksheet():

    with open('config.json', encoding='utf-8') as config:
        data = json.load(config)

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    my_credentials = service_account.Credentials.from_service_account_file('key.json', scopes=scopes)

    auth = gs.authorize(my_credentials)
    sheet = auth.open_by_url(data['sheet'])

    return sheet.get_worksheet(0)
