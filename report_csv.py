import os
import csv

class ReportToCsv:
    def __init__(self,username,status,reason,unique):
        self.username = username
        self.status = status
        self.reason = reason
        self.unique = unique
        self.fldnames = ["username","status","reason","unique"]

    def reporting(self):
        with open("report.csv","a",newline="") as report:
            writing = csv.writer(report)
            
            # writing.writerow(self.fldnames)
            writing.writerow([self.username,self.status,self.reason,self.unique])




# reporting = ReportToCsv("haha@ga.com","added","added",False)
# reporting.reporting()
reporting = ReportToCsv("haha@gaga.com","error","error",True)
reporting.reporting()