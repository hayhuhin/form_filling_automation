from pathlib import Path
import csv
from datetime import datetime

class ReportToCsv:
    def __init__(self,username,status,reason,unique:True):
        self.username = username
        self.status = status
        self.reason = reason
        self.unique = unique
        self.date = datetime.now()
        self.path = Path("report.csv")

    def  reporting(self):
        with open(self.path,"r+",newline="") as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            for user,status,reason,unique,date in data:
                if self.username == user:
                    self.unique = False




        with open(self.path,"a",newline="") as report:
            writing = csv.writer(report)
            
            # writing.writerow(self.fldnames)
            writing.writerow([self.username,self.status,self.reason,self.unique,self.date])
        print(f"username: {self.username} is {self.status}. reason>> {self.reason}")



# test = ReportToCsv("sergei","no status","just a test",True)
# test.reporting()

