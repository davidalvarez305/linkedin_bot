import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .auth import get_auth

def write_values(spreadsheet_id, range, values):
    try:
        credentials = get_auth()
        service = build('sheets', 'v4', credentials=credentials)

        sheet = service.spreadsheets()

        body = {
            "values": values
        }

        sheet.values().update(
            spreadsheetId=spreadsheet_id, range=range,
            valueInputOption="USER_ENTERED", body=body).execute()
    except HttpError as err:
        print(err)

def get_values(spreadsheet_id, range):
    try:
        credentials = get_auth()
        service = build('sheets', 'v4', credentials=credentials)

        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range).execute()
        values = result.get('values', [])

        if not values:
            return []

        return values
    except HttpError as err:
        print(err)