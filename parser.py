import gspread
# import os
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'token.json'
SPREADSHEET_ID = '1d8qVc3Ayt1O1eBU-ikcXrbLvCLHWawpd5WPniVajmRc'
# API_KEY = 'AIzaSyAePMFRM8fGCQ8oYEUnWxL7UVFyXWYh6DY'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

client = gspread.service_account(filename='token.json')

sheet = client.open_by_key(SPREADSHEET_ID)
worksheet = sheet.get_worksheet(0)
result = worksheet.get_all_records()
print(result)


# credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     CREDENTIALS_FILE, SCOPES)
# httpAuth = credentials.authorize(httplib2.Http())
# service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)
# sheet = service.spreadsheets()
# result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                                     range='Лист1!F1:AM').execute()
# print(result)