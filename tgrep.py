import sys
import re
class lineDate:
    def __init__(self, date_line):
        self.line = date_line
        matches = re.match('^([A-Za-z]{3})\s+([0-9]{1,2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', self.line)
        self.month = matches.group(1)
        self.day = matches.group(2)
        self.hour = matches.group(3)
        self.minute = matches.group(4)
        self.second = matches.group(5)

if __name__ == "__main__":
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    file = open(filename, "r")

    for line in file:
        print line
        ld = lineDate(line)
        print ld.month
        print ld.day
        print ld.hour
        print ld.minute
        print ld.second
