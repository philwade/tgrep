import sys
import re
class lineDate:
    def __init__(self, date_line):
        self.line = date_line
        self.hour = None
        self.minute = None
        self.second = None
        try:
            matches = re.search('^([0-9]{2}):?| ([0-9]{2}):', self.line)
            self.hour = matches.group(1) or matches.group(2)
            matches = re.search('[0-9]{2}:(?P<minute>[0-9]{2}):?', self.line)
            self.minute = matches.group('minute')
            matches = re.search('[0-9]{2}:[0-9]{2}:(?P<second>[0-9]{2})', self.line)
            self.second = matches.group('second')
        except AttributeError:
            if self.hour == None:
                raise TypeError("Not a parsable date")

    def __str__(self):
        if self.second != None:
            return ":".join([self.hour, self.minute, self.second])
        elif self.minute != None:
            return ":".join([self.hour, self.minute])
        else:
            return self.hour

    def __lt__(self, other):
        if self.hour < other.hour:
            return True
        elif self.hour == other.hour:
            if self.minute == None or self.minute < other.minute:
                return True
            elif self.minute == other.minute:
                if self.second == None or self.second < other.second: 
                    return True 
                else: 
                    return False
            else:
                return False
        else:
            return False

    def __gt__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other): 
        if self.hour == other.hour:
            if self.minute == None or other.minute == None:
                return True
            elif self.minute == other.minute:
                if self.second == None or other.second == None or self.second == other.second:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

class searchRange:
    def __init__(self, date_line):
        dates = date_line.split('-')
        self.start = lineDate(dates[0])
        self.end = lineDate(dates[1])
    def __gt__(self, other):
        if self.start > other:
            return True
        else:
            return False
    def __lt__(self, other):
        if self.end < other:
            return True
        else:
            return False
    def __eq__(self, other):
        if self.start < other and self.end > other:
            return True
        else:
            return False

if __name__ == "__main__":
    search = None
    filename = "sample.log" #default
    try:
        arg1 = sys.argv[1]
    except IndexError:
        raise Exception("I need at least a timestamp to look for")
    try:
        arg2 = sys.argv[2]
    except IndexError:
        arg2 = None

    try:
        search = searchRange(arg1)
        if arg2 != None:
            filename = arg2
    except IndexError:
        try:
            search = searchRange(arg2)
            filename = arg1
        except (IndexError, AttributeError):
            try:
                search = lineDate(arg1)
                if arg2 != None:
                    filename = arg2
            except TypeError:
                if arg2 != None:
                    search = lineDate(arg2)
                    filename = arg1
                else:
                    raise Exception("I need at least a timestamp to look for")

    file = open(filename, "r")

    for line in file:
        ld = lineDate(line)
        if(ld > search):
            print line

    print search
