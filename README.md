# RoastingComputer
This is the repository for Good Citizen Coffee Co's roasting computers in order for them to work with RoastingBot. This way, all they need to do is clone this repo, add some configs on their end, and they are good to go! 

This is a new repo so that the full RoastingBot program can be separated from the users. 

## Needed Files for Operation
### 1 - config.py File
This file must have the following variables
- ssName : The name of the spreadsheet you will be using (ex: Roast Sheet 2.4.7)
- wsName : The name of the tab on that sheet (ex: Roast Sheet)
- dir : The directory that roast files will be saved to (ex: C:/Users/Roaster/Desktop/RoastLogs)
- dest : The directory that the processed files will be moved to (ex: C:/Users/Roaster/Desktop/FormattedRoastLogs)
- repoDir : The Directory of the repository (ex: C:/Users/Roaster/Documents/RoastingComputer)
- machine : This is the color of the roaster (ex: "White" or "Red")

### 2 - creds.json File
This file is generated when a new Google Sheets API account is created with Google. In this file is an email address that needs to have access to the google sheet you will be working on. 

[Tech with Tim](https://www.youtube.com/watch?v=cnPlKLEGR7E) has a great video on how to get that set up.

### 3 - .gitignore File 
Make sure that there is a .gitignore file with the config and creds file in there. <b>Please include any test files in there as to not clutter the repository.</b>

## Computer Set Up
You will need to do a few things to set up your computer. 
- Install [Artisan](https://artisan-scope.org/)
- Install [Phidget Drivers](https://www.phidgets.com/docs/OS_-_Windows)
- Install a text editor like VSCode or Notepad ++
- Clone the Repo to the computer
- Create the necessary files from above

To make things easier for the users, I will also create a .bash_profile file that has a few aliases to easily get the script up and running. Typically the aliases will be something like "go" or "start". Those will navigate to the correct directory and run the python monitor script. 