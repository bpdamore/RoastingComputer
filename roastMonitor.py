# This script monitors the folder that holds all the roasting files. 

import time,re,os,shutil
from fuzzywuzzy import fuzz
from tkinter import Tk
from tkinter.messagebox import Message 
from _tkinter import TclError
from easygui import enterbox

# Import G-sheet stuff
import gspread
from  oauth2client.service_account import ServiceAccountCredentials

from config import dir, dest, ssName, wsName, repoDir
from monitorFunc import *

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet=client.open(ssName).worksheet(wsName)

# Create the search for the weight, title, and blend component
batchSearch = re.compile(r"'weightin': (\d+)")
coffeeSearch = re.compile(r"'title': '([a-zA-Z ]+)(\d+)?',")
blendSearch = re.compile(r"'beans': '([a-zA-Z ]+)',")
roasterSearch = re.compile(r"'operator': '([a-zA-Z]+)'")

# Make sure it is operating in the correct directory
os.chdir(dir)

# Keep it always running
run = True
print("\n\nStarting up ...")
print("Monitoring roasts ... ")

while run == True:

    if len(os.listdir()) == 0:
        pass
    else:
        # Now we need to make sure that there is no conflict between multiple machines
        wait = True
        while wait:
            # Check the 'On Air' cell 
            data = sheet.acell('B1').value
            if data == 'Processing':
                print('\nwaiting 15 seconds...')
                time.sleep(15)
            # When the cell is blank, go forward. 
            else:
                # Make it processing before getting going
                sheet.update("B1","Processing")
                wait = False
        # For each file in the dir path...
        for f in os.listdir():
            sheet=client.open(ssName).worksheet(wsName)
            data = sheet.get_all_values()
            with open(f,"r") as x:
                text = x.read()
                batch = int(batchSearch.search(text).group(1).strip())
                cname = coffeeSearch.search(text).group(1).strip()
                roaster = roasterSearch.search(text).group(1).strip()
                blendname = "SO"
                # try:
                #     blendname = blendSearch.search(text).group(1).strip()
                # except:
                #     blendname = "SO"
                print("\n\nFound the following from the file: ")
                print(f"Batch size : {batch}")
                print(f"Coffee name : {cname}")
                print(f"Blend : {blendname}")

            f_name,f_ext = os.path.splitext(f)
            try:
                f_coffee,f_date,f_time = f_name.split('_')
                f_year,f_month,f_day = f_date.split('-')
                new_name = '{}-{}_{}-{}-{}_{}{}'.format(f_coffee,batch,f_month,f_day,'20'+f_year,f_time,f_ext)
                os.rename(f,new_name)
            except ValueError:
                new_name = f
                print(f + " was not processed")

            # Match is starting out as the 'no match found' option.
            match = 4

            while match == 4:
                
                # Change to the repo directory before running the RoastMatch function
                os.chdir(repoDir)
                match, SOmatch = RoastMatch(data,cname,batch,match,roaster,blendname,sheet)
                
                if match == 1:
                    # If there was a SO match...
                    TIME_TO_WAIT = 4500 # in milliseconds
                    root = Tk() 
                    root.withdraw()
                    try:
                        root.after(TIME_TO_WAIT, root.destroy) 
                        Message(title="Roast Added!", message=f"Added {batch}lb to {SOmatch}!", master=root).show()
                        root.wm_attributes("-topmost", 1) 
                        root.focus()   
                    except TclError:
                        pass
                    
                elif match == 2:
                    # If there was a Chin Up match
                    TIME_TO_WAIT = 4500 # in milliseconds 
                    root = Tk() 
                    root.withdraw()
                    try:
                        root.after(TIME_TO_WAIT, root.destroy) 
                        Message(title="Roast Added!", message=f"Added {batch}lb to {SOmatch}, and to the Chin Up Pre-Post count!", master=root).show()
                    except TclError:
                        pass

                elif match == 3:
                    TIME_TO_WAIT = 4500 # in milliseconds 
                    root = Tk() 
                    root.withdraw()
                    try:
                        root.after(TIME_TO_WAIT, root.destroy) 
                        Message(title="Roast Added!", message=f"Added {batch}lb to {SOmatch}, and to the Buckle Down Pre-Post count!", master=root).show()
                    except TclError:
                        pass
                    
                elif match == 4:
                    # No match, so get the right coffee name, and try again
                    cname = enterbox("No match found!\nWhat coffee did you just roast?")

            os.chdir(dir)
            print("\nMoving file to Formatted Roast Logs folder")
            shutil.move(dir+"/"+new_name,dest)
        sheet.update("B1","")
        print("\nDone!")

    time.sleep(30)