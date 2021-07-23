# Author: Diego Lopez
# Date: 07-09-2021
# This file 

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
from datetime import date
from time_room import *

def deploy_update ():
    scopes = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("discord_bot.json", scopes) #access the json key you downloaded earlier 
    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    sheet = file.open("Maintenance Sheet Sample")  #open sheet
    sheet = sheet.worksheet(str(date.today()))
    """
    Cell 1: Deploy Before Times - start time of a class that needs a mic / absolute latest time to deploy a mic
    Cell 2: Rooms               - these appear 1 row after a entry in Cell A
                                - entries may exist under a certain time until a new entry in Cell A or the end of the sheet
    Cell 3: Quantity            - how many mics to be deployed
    Cell 4: Deployed            - checked if staff marked the mic as deployed
    Cell 5: Deployed By         - name of staff member who did the deployment ie who to blame if something goes wrong
    Cell 6: Comments            - any comments made by staff relating to relevant room 
    Cell 7: Empty
    """
    values_list = enumerate(sheet.col_values(1), start=1)
    deploy_times = []
    for value in values_list:
        if value[1] and value[1] != "Deploy Before":
            print(value[1])
            time_counter = value[0] + 1
            curr_dep = deploy_time(date.today(), value[1])
            while sheet.cell(time_counter,1).value is None and sheet.cell(time_counter,2).value is not None:
                print(sheet.cell(time_counter,2).value)
                curr_dep.rooms.append(deploy_room(sheet.cell(time_counter,2).value, sheet.cell(time_counter,3).value, sheet.cell(time_counter,4).value, 
                sheet.cell(time_counter,5).value, sheet.cell(time_counter,6).value))
                time_counter += 1
            deploy_times.append(curr_dep)
    return deploy_times

def check_update (): 
    scopes = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("discord_bot.json", scopes) #access the json key you downloaded earlier 
    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    sheet = file.open("Maintenance Sheet Sample")  #open sheet
    sheet = sheet.worksheet(str(date.today())) # assumption that a new sheet is created per day of the format Year-Month-Day
    """
    Cell 8: Check battery betw. - 2 times indicating earliest and latest times to check battery in a room
    Cell 9: Rooms               - these appear 1 row after a entry in Cell H
                                - entries may exist under a certain time until a new entry in Cell H or the end of the sheet
    Cell 10: Checked             - checked if staff member marked the batteries as checked
    Cell 11: Checked by          - name of staff member who did the battery check
    Cell 12: Comments            - any comments made by staff relating to relevant room
    """
    values_list = enumerate(sheet.col_values(8), start=1)
    check_times = []
    for value in values_list:
        if value[1] and value[1] != "Check battery between":
            # print(value[1])
            time_counter = value[0] + 1
            times = value[1].split("-")
            curr_check = check_time(date.today(), times[0], times[1])
            while sheet.cell(time_counter,8).value is None and sheet.cell(time_counter,9).value is not None:
                #print(sheet.cell(time_counter,9).value)                
                curr_check.rooms.append(check_room(sheet.cell(time_counter,9).value, sheet.cell(time_counter,10).value, sheet.cell(time_counter,11).value, 
                sheet.cell(time_counter,12).value))
                time_counter += 1
            check_times.append(curr_check)
    return check_times

"""
x = deploy_update()
for elem in x:
    e = str(elem)
    print(e)
"""