# Author: Diego Lopez
# Date: 07-10-2021
# Notes: This file contains necessary classes for containing and organizing information gathered from the google sheet

class room (object):
    def __init__ (self, room_name, comments):
        # room_name: A string of the room name
        # comments: A string of any information that is important but not characterized by the other attr
        self.room_name = room_name
        self.comments  = comments
    def __repr__(self):
        return f"Room: {self.room_name}\nComments: {self.comments}+\n"

class deploy_room (room):
    def __init__ (self, room_name, quantity, is_deployed, deployed_by, comments):
        # quantity: A integer of the number of mics to be left in the room
        # is_deployed: A bool of whether or not the mics have been deployed to room
        # deployed_by: A string containing the name of whoever deployed the mic - empty if not yet deployed
        super().__init__(room_name, comments)
        self.deployed_by = deployed_by 
        self.quantity    = quantity
        self.is_deployed = is_deployed
    def __repr__(self):
        return f"{super().__repr__()}Deployed by: {self.deployed_by}\nQuantity: {self.quantity}\nDeployed: {self.is_deployed}\n" 

class check_room (room):
    def __init__ (self, room_name, is_checked, checked_by, comments):
        # is_checked: A bool of whether or not the batteries in the mic(s) have been checked
        # checked_by: A string containing the name of whoever checked the batteries of the mic - empty if not yet checked
        super().__init__ (room_name, comments)
        self.is_checked = is_checked
        self.checked_by = checked_by
    def __repr__(self):
        return f"{super().__repr__()}Checked: {self.is_checked}\nChecked by: {self.checked_by}\n"

class deploy_time (object):
    def __init__(self, date, time):
        # date: A Date object containing the date which this deploy time is active
        # time: A string containing the last possible time that a mic must be deployed to the room(s) in the attr
        # rooms: Contains a list of room objects that fall under this deploy time
        self.date  = date
        self.time  = time
        self.rooms = []
    def __repr__(self):
        header = f"{self.date}\n{self.time}\n"
        rep = ""
        for elem in self.rooms:
            rep += repr(elem)
        return header + rep

class check_time (object):
    def __init__(self, date, time_start, time_end):
        # date: A Date object containing the date which this deploy time is active
        # time_start: A string containing the earliest that a room can have batteries checked
        # time_end: A string containing the latest time that a room can have batteries checked
        # rooms: Contains a list of room objects that fall under this check time
        self.date        = date
        self.time_start  = time_start
        self.time_end    = time_end
        self.rooms       = []
    def __repr__(self):
        header = f"{self.date}\n{self.time_start}\n{self.time_end}\n"
        rep = ""
        for elem in self.rooms:
            rep += repr(elem)
        return header + rep


