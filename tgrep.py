#tgrep.py by phil wade (phil@philwade.org) 
import sys
import re
from os.path import getsize
DEBUG = False

class lineDate:
    def __init__(self, date_line):
        self.line = date_line
        self.hour = None
        self.minute = None
        self.second = None
        self.zeroThreshold = "12" #pivot number where decide to think of 00 as 0 or 24...
        try:
            matches = re.search('^([0-9]{1,2}):?| ([0-9]{2}):', self.line)
            self.hour = matches.group(1) or matches.group(2)
            if len(self.hour) == 1:
                self.hour = "0" + self.hour
            matches = re.search('[0-9]{1,2}:(?P<minute>[0-9]{2}):?', self.line)
            self.minute = matches.group('minute')
            matches = re.search('[0-9]{1,2}:[0-9]{2}:(?P<second>[0-9]{2})', self.line)
            self.second = matches.group('second')
        except AttributeError:
            if self.hour == None:
                raise TypeError("Not a parsable date: %s" % self.line)

    def __str__(self):
        if self.second != None:
            return ":".join([self.hour, self.minute, self.second])
        elif self.minute != None:
            return ":".join([self.hour, self.minute])
        else:
            return self.hour

    def __lt__(self, other):
        selfHourValue = self.hour
        otherHourValue = other.hour
        if other.hour == "00":
            if self.hour > self.zeroThreshold:
                otherHourValue = "24"

        if self.hour == "00":
            if other.hour > self.zeroThreshold:
                selfHourValue = "24"

        if selfHourValue < otherHourValue:
            return True
        elif selfHourValue == otherHourValue:
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

    def __gte__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lte__(self, other):
        return self.__lt__(other) or self.__eq__(other)

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
    def __init__(self, filename, search, searchEnd=None):
        self.range = False
        self.debug = True
        if searchEnd != None:
            self.range = True
            self.searchEnd = searchEnd
        self.file = open(filename, "r")
        self.fileEnd = getsize(filename)
        self.fileStart = 0
        self.firstDate = lineDate(self.file.readline())
        self.file.seek(self.fileEnd - 200)
        self.file.readline() 
        self.lastDate = lineDate(self.file.readline())
        if DEBUG:
            print "First: ", self.firstDate, " Last: ", self.lastDate
        self.linearThreshHold = 1000
        self.backStep = 72
        self.search = search
        self.firstPivot = self.fileEnd / 2
        self.file.seek(self.firstPivot)
        self.file.readline() 
        self.midDate = lineDate(self.file.readline())
        self.searchBothHalves = False
        self.checkHalves()

    def checkHalves(self): #see if we need to check both halves
        if self.range:
            if self.search < self.firstDate and self.searchEnd > self.lastDate \
            or self.search < self.firstDate and self.searchEnd > self.firstDate \
            or self.search > self.firstDate and self.searchEnd < self.lastDate \
            or self.search < self.lastDate or self.search == self.lastDate and self.searchEnd > self.lastDate \
            or self.search < self.firstDate:
                if DEBUG:
                    print "DEBUG: range that spans both halves"
                self.searchBothHalves = True
        else:
            if self.search < self.lastDate and self.search > self.firstDate \
            or self.search == self.lastDate or self.search == self.firstDate:
                if DEBUG:
                    print "DEBUG: value that spans both halves"
                self.searchBothHalves = True

    def seekDateBetween(self, start=None, end=None):
        if start == None and end == None:
            start = self.fileStart
            end = self.fileEnd
            if self.searchBothHalves:
                self.seekDateBetween(self.fileStart, self.firstPivot)
                self.seekDateBetween(self.firstPivot, self.fileEnd)
                return
        searchsize = end - start
        pivot = (end - start) / 2 + start
        if DEBUG:
            print "DEBUG: ", start, end
        if searchsize > self.linearThreshHold:
            self.file.seek(pivot)
            self.file.readline() #throw away read because we won't get a full line
            testline = self.file.readline()
            testdate = lineDate(testline)
            if DEBUG:
                print "DEBUG: ", testline
            if self.equalSearch(testdate):
                return self.linearSearch(start, end, True) #in case we land in the middle of our search

            if self.lessThanSearch(testdate):
                return self.seekDateBetween(pivot, end)
            elif self.greaterThanSearch(testdate):
                return self.seekDateBetween(start, pivot)
            else:
                print "something terrible has happened"
        else:
            self.linearSearch(start, end)

    def seekBack(self):
        while True:
            current = self.file.tell()
            newPlace = current - (self.backStep * 20)
            if newPlace < 0:
                return 0
                break
            self.file.seek(newPlace)
            self.file.readline()
            test = lineDate(self.file.readline())
            if DEBUG:
                print "DEBUG: jump back date: ", test
            if not self.equalSearch(test):
                break
        newStart = self.file.tell()
        newStart = newStart - self.backStep
        return newStart

    def linearSearch(self, start, end, landedOn=False):
        if landedOn:
            start = self.seekBack()
        if DEBUG:
            print "DEBUG: Linear searching between ", start, " ", end 
        looking = True
        matched = False
        self.file.seek(start)
        if start != 0:
            self.file.readline() #get a fresh line when we start looping
        while looking and self.file.tell() < end:
            line = self.file.readline()
            test = lineDate(line)
            if self.equalSearch(test):
               print line,
               matched = True
            elif matched:
                looking = False
        if matched:
            return True
        else:
            return False

    def lessThanValue(self, testdate, search):
        if (search > self.firstDate or search == self.firstDate) and (search < self.lastDate or search == self.lastDate):
            if testdate < self.midDate:
                return testdate < search
            else:
                return True
        elif testdate < self.firstDate and search > self.firstDate:
            return False
        elif testdate > self.firstDate and search < self.firstDate:
            return True
        else:
            return testdate < search

    def lessThanSearch(self, testdate):
        if self.range:
            return self.lessThanValue(testdate, self.search)
        else:
            return self.lessThanValue(testdate, self.search)

    def greaterThanValue(self, testdate, search):
        if (search > self.firstDate or search == self.firstDate) and (search < self.lastDate or search == self.lastDate):
            if testdate < self.midDate:
                return testdate > search
            else:
                return False
        elif testdate < self.firstDate and search > self.firstDate:
            return True
        elif testdate > self.firstDate and search < self.firstDate:
            return False
        else:
            return testdate > search

    def greaterThanSearch(self, testdate):
        if self.range:
            return self.greaterThanValue(testdate, self.search)
        else:
            return self.greaterThanValue(testdate, self.search)

    def equalSearch(self, testdate):
        if self.range:
            if self.lessThanValue(testdate, self.searchEnd) and self.greaterThanValue(testdate, self.search) or testdate == self.search or testdate == self.searchEnd:
                return True
        else:
            if testdate == self.search:
                return True
        return False

def parseDateArg(arg):
    end = None
    dates = arg.split('-')
    search = lineDate(dates[0])
    if len(dates) == 2:
        end = lineDate(dates[1])
    return search, end
    
    
if __name__ == "__main__":
    search = None
    end = None
    filename = "/logs/haproxy.log" #default
    try:
        arg1 = sys.argv[1]
    except IndexError:
        raise Exception("I need at least a timestamp to look for")
    try:
        arg2 = sys.argv[2]
    except IndexError:
        arg2 = None

    try:
        search, end = parseDateArg(arg1)
        if arg2 != None: 
            filename = arg2
    except TypeError: #arg1 is not a date of any type
        if arg2 == None: #we got no dates i guess, fail hard
            raise Exception("I need at least a timestamp to look for")
        else:
            search, end = parseDateArg(arg2)
            filename = arg1

    hp = seeker(filename, search, end)
    hp.seekDateBetween()
