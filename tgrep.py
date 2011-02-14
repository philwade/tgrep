import sys
import re
class lineDate:
    def __init__(self, date_line):
        self.line = date_line
        self.hour = None
        self.minute = None
        self.second = None
        try:
            matches = re.search('(?P<hour>[0-9]{2}):?', self.line)
            self.hour = matches.group('hour')
            matches = re.search('[0-9]{2}:(?P<minute>[0-9]{2}):?', self.line)
            self.minute = matches.group('minute')
            matches = re.search('[0-9]{2}:[0-9]{2}:(?P<second>[0-9]{2})', self.line)
            self.second = matches.group('second')
        except AttributeError:
            if self.hour == None:
                raise TypeError("Not a parsable date")

if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
    except IndexError:
        pass

    filename = arg1
    file = open(filename, "r")

    for line in file:
        print line
        ld = lineDate(line)
        print ld.hour
        print ld.minute
        print ld.second
