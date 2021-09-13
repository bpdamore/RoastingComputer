# Holds any sort of diary scripts needed

# Update the google Sheet with events
def DiaryUpdate(event):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    from config import key, password, hostname, version, emPass

    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)


    # Choose the sheet/worksheet that you will be working on
    # sheet = client.open("test").worksheet(ws)
    sheet = client.open('Roast Sheet 2.4.7')
    entry = sheet.values_get(range="Diary!A1:D")['values']
    entry.append(event)
    sheet.values_update('Diary!A1:D',params={'valueInputOption':'USER_ENTERED'},body={'values':entry})

# Creates the row entry.
def dearDiary(words,roaster):
    from datetime import datetime
    today = datetime.today()
    d,t = str(today).split(' ')
    event = [d,t,words,roaster]
    return event

