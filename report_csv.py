import os
import csv

class ReportToCsv:
    def __init__(self,username,status,reason,unique:True):
        self.username = username
        self.status = status
        self.reason = reason
        self.unique = unique
        self.fldnames = ["username","status","reason","unique"]

    def  reporting(self):
        with open("form_filling_automation/report.csv","r+",newline="") as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            for user,status,reason,unique in data:
                if self.username == user:
                    self.unique = False




        with open("form_filling_automation/report.csv","a",newline="") as report:
            writing = csv.writer(report)
            
            # writing.writerow(self.fldnames)
            writing.writerow([self.username,self.status,self.reason,self.unique])
        print(f"username: {self.username} is {self.status}. reason>> {self.reason}")



# test = ReportToCsv("sergei","no status","just a test",True)
# test.reporting()
