import sys
import re
from os.path import getsize
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

class seeker:
    def __init__(self, filename, search):
        self.file = open(filename, "r")
        self.fileEnd = getsize(filename)
        self.fileStart = 0
        self.linearThreshHold = 1000
        self.search = search

    def seekDateBetween(self, start=None, end=None):
        if start == None:
            start = self.fileStart
        if end == None:
            end = self.fileEnd
        searchsize = end - start
        print start, end
        if searchsize > self.linearThreshHold:
            pivot = (end - start) / 2 + start
            self.file.seek(pivot)
            self.file.readline() #throw away read because we won't get a full line
            testdate = lineDate(self.file.readline())
            print testdate

            if testdate < search:
                return self.seekDateBetween(pivot, end)
            elif testdate > search:
                return self.seekDateBetween(start, pivot)
        else:
            self.linearSearch(start, end)

    def linearSearch(self, start, end):
        looking = True
        matched = False
        self.file.seek(start)
        self.file.readline() #get a fresh line when we start looping
        while looking:
            line = self.file.readline()
            test = lineDate(line)
            if test == self.search:
               print line 
               matched = True
            elif matched:
                looking = False
    
if __name__ == "__main__":
    search = None
    range = False
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
        dates = arg1.split('-')
        start = lineDate(dates[0])
        end = lineDate(dates[1])
        range = True
    except (IndexError, TypeError):
        if arg2 != None:
            try:
                dates = arg2.split('-')
                start = lineDate(dates[0])
                end = lineDate(dates[1])
                range = True
            except (IndexError, TypeError):
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
        else:
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


    hp = seeker(filename, search)
    hp.seekDateBetween()
