# Author: Diego Lopez
# Date: 07-09-2021
# This file 

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
from datetime import date
from time_room import *
import pandas as pd 

def deploy_update_full():
    scopes = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("discord_bot.json", scopes) #access the json key you downloaded earlier 
    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    sheet = file.open("Maintenance Sheet Sample")  #open sheet
    """
    Cell 0: Deploy Before Times - start time of a class that needs a mic / absolute latest time to deploy a mic
    Cell 1: Rooms               - these appear 1 row after a entry in Cell A
                                - entries may exist under a certain time until a new entry in Cell A or the end of the sheet
    Cell 2: Quantity            - how many mics to be deployed
    Cell 3: Deployed            - checked if staff marked the mic as deployed
    Cell 4: Deployed By         - name of staff member who did the deployment ie who to blame if something goes wrong
    Cell 5: Comments            - any comments made by staff relating to relevant room 
    Cell 6: Empty
    """
    sheet = sheet.worksheet(str(date.today()))
    df = pd.DataFrame(sheet.get_all_values())
    current_times = []
    for i in range(len(df[0])):
        if df.iloc[i,0] and df.iloc[i,0] != "Deploy Before":
            #print(df.iloc[i,0])
            time_counter = i + 1
            current_deployment = deploy_time(date.today(), df.iloc[i,0])
            while time_counter < len(df[1]) and df.iloc[time_counter, 0] == "":
                print(df.iloc[time_counter,1])
                current_deployment.rooms.append(deploy_room(df.iloc[time_counter, 1], df.iloc[time_counter, 2], df.iloc[time_counter, 3]
                , df.iloc[time_counter, 4], df.iloc[time_counter, 5]))
                time_counter += 1
            current_times.append(current_deployment)
    return current_times

def check_update_full():
    scopes = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("discord_bot.json", scopes) #access the json key you downloaded earlier 
    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    sheet = file.open("Maintenance Sheet Sample")  #open sheet
    """
    Cell 7: Check battery betw. - 2 times indicating earliest and latest times to check battery in a room
    Cell 8: Rooms               - these appear 1 row after a entry in Cell H
                                 - entries may exist under a certain time until a new entry in Cell H or the end of the sheet
    Cell 9: Checked             - checked if staff member marked the batteries as checked
    Cell 10: Checked by          - name of staff member who did the battery check
    Cell 11: Comments            - any comments made by staff relating to relevant room
    """
    sheet = sheet.worksheet(str(date.today()))
    df = pd.DataFrame(sheet.get_all_values())
    current_times = []
    print(df)
    for i in range(len(df[7])):
        if df.iloc[i,7] and df.iloc[i,7] != "Check battery between":
            time_counter = i + 1
            time = df.iloc[i,7].split("-")
            current_check = check_time(date.today(), time[0], time[1])
            while time_counter < len(df[8]) and df.iloc[time_counter, 7] == "" and df.iloc[time_counter, 8] != "":
                current_check.rooms.append(check_room(df.iloc[time_counter, 8], df.iloc[time_counter, 9], df.iloc[time_counter, 10]
                , df.iloc[time_counter, 11]))
                time_counter += 1
            current_times.append(current_check)
    return current_times

x = check_update_full()
for elem in x:
    e = str(elem)
    print(e)
