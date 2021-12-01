import json
from google.oauth2 import service_account
import gspread as gs

with open('config.json', encoding='utf-8') as config:
    config = json.load(config)

_scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

_my_credentials = service_account.Credentials.from_service_account_file('key.json', scopes=_scopes)
_auth = gs.authorize(_my_credentials)

async def get_worksheet():
    try:
        sheet = _auth.open_by_url(config['sheet'])
        return sheet.get_worksheet(0)

    except:
        return await get_worksheet()
