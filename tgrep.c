#include <stdio.h>
#include <regex.h>
#include <string.h>
#include <stdlib.h>

typedef struct lineDate {
    int hour;
    int minute;
    int second;
    struct lineDate* secondDate;
} lineDate;

int matchAndParseInt(char* timeString, char* timePattern)
{
    regex_t re;
    regmatch_t matches[2];

    if(regcomp(&re, timePattern, REG_EXTENDED) != 0)
    {
        printf("Failed to compile regex");
    }


    if(regexec(&re, timeString, 2, matches, 0) == 0)
    {
        int matchSize = (int)(matches[1].rm_eo - matches[1].rm_so);
        char match[matchSize];
        strncpy(match, timeString + (int)matches[1].rm_so, matchSize);
        printf("Match: %s\n", match);
        regfree(&re);
        return atoi(match);
    }
    regfree(&re);
    return -1;
}

//only pass in single time as timeString
void populateLineDate(lineDate* time, char* timeString)
{
    char* hourPattern = "^([0-9]{1,2}):?| ([0-9]{2}):";
    char* minutePattern = "[0-9]{1,2}:([0-9]{2}):?";
    char* secondPattern = "[0-9]{1,2}:[0-9]{2}:([0-9]{2})";
    time->hour = matchAndParseInt(timeString, hourPattern);
    if(time->hour != -1)
    {
        time->minute = matchAndParseInt(timeString, minutePattern);
        if(time->minute != -1)
        {
            time->second = matchAndParseInt(timeString, secondPattern);
        }
    }
}

void buildLineDate(lineDate* myDate, char* inputTimeString)
{
    myDate = (lineDate*) malloc(sizeof(lineDate));
    int secondTimeOffset;
    char* firstDate;
    char* secondDate;

    if(isRange(inputTimeString, &secondTimeOffset) != 0)
    {
        firstDate = (char*) malloc(strlen(inputTimeString) - secondTimeOffset);
        secondDate = (char*) malloc(secondTimeOffset);
        strcpy(firstDate, inputTimeString+secondTimeOffset);
        strncpy(secondDate, inputTimeString, --secondTimeOffset);
        populateLineDate(myDate, firstDate);
        myDate->secondDate = (lineDate*) malloc(sizeof(lineDate));
        populateLineDate(myDate->secondDate, secondDate);
        printf("first: %s, second %s\n", firstDate, secondDate);
        free(secondDate);
    }
    else
    {
        firstDate = (char*) malloc(strlen(inputTimeString));
        strcpy(firstDate, inputTimeString);
        populateLineDate(myDate, firstDate);
        printf("first: %s\n", firstDate);
    }
    free(firstDate);
}


int isRange(char* inputTime, int* offset)
{
    int i;
    for(i = 0;i < strlen(inputTime);i++)
    {
        if(*(inputTime + i) == '-')
        {
            *offset = ++i;
            return i;
        }
    }

    return 0;
}

int main(int argc, char* argv[])
{
    lineDate* date;
    date = (lineDate*) malloc(sizeof(lineDate));

    if(argc == 1)
    {
        printf("I need at least a timestamp to look for\n");
        return 1;
    }

    buildLineDate(date, argv[1]);
    if(date->hour == -1 && argc > 2)
    {
        buildLineDate(date, argv[2]);
        if(date->hour == -1)
        {
            printf("Bad timestamp or no timestamp given.\n");
            return 1;
        }
    }
    else
    {
        printf("Got a date in the first arg\n");
        return 1;
    }
    //printf("%i \n", date.hour);
    free(date->secondDate);
    free(date);
    return 0;
}


