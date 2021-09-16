# Holds any sort of diary scripts needed

# Update the google Sheet with events
def DiaryUpdate(event):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    from config import dir, dest, ssName, wsName

    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)


    # Choose the sheet/worksheet that you will be working on
    # sheet = client.open("test").worksheet(ws)
    sheet=client.open(ssName)
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

# Create matching function
def RoastMatch(data,cname,batch,match,roaster,blendname,sheet):
    """
    data == sheet data
    cname == coffee name
    batch == batch weight 
    """
    from fuzzywuzzy import fuzz
    row = 0
    for x in data:
        if match != 4:
            pass
        else:
            if "dark" not in cname.lower() and "dark" in x[0].lower():
                row+=1
                pass

            elif "dark" in cname.lower() and "dark" not in x[0].lower():
                row+=1
                pass

            else: 
                perc = fuzz.partial_ratio(cname.lower(),x[0].lower())
                if perc >= 80:
                    # print(f"{perc} -> {x[0]}")
                    print(f"\nMatched {cname} to {x[0]} with {perc}% certainty")
                    SOmatch = x[0]
                    # print(f"row {row}\n")
                    totRoast = x[3]
                    if totRoast == "":
                        totRoast = 0
                    else: 
                        totRoast = int(totRoast)

                    # Keep a record
                    logmsg = f"Changing {x[0]}'s roasted lbs from {totRoast} to {totRoast+batch}"
                    event = dearDiary(logmsg, roaster)
                    DiaryUpdate(event)
                    # print(event)
                    totRoast+=batch
                    # print(totRoast)
                    print(logmsg)
                    sheet.update_cell(row+1,4,totRoast)
                    match = 1

                    # print(match)

                    if blendname != "SO":
                        chinperc = fuzz.partial_ratio(blendname.lower(),"chin up")
                        buckperc = fuzz.partial_ratio(blendname.lower(),"buckle down")

                        if chinperc > buckperc:
                            num = sheet.cell(54,3).value
                            if num == "":
                                num = 0
                            else:
                                num = int(num)
                            num+=batch
                            sheet.update_cell(54,3,num)
                            blendmsg = f"Added {batch} to Chin Up"
                            event = dearDiary(blendmsg, "")
                            DiaryUpdate(event)
                            print(event)
                            match = 2

                        # if buckperc > chinperc:
                        #     num = sheet.cell(55,3).value
                        #     if num == "":
                        #         num = 0
                        #     else:
                        #         num = int(num)
                        #     num+=batch
                        #     sheet.update_cell(55,3,num)
                        #     blendmsg = f"Added {batch} to Buckle Down"
                        #     event = dearDiary(blendmsg,"")
                        #     DiaryUpdate(event)
                        #     print(event)
                        #     match = 3

                elif perc < 80:
                    # print(f"Not sure about this one...")
                    SOmatch = "nah"
                    match = 4

                row+=1

    return match, SOmatch
