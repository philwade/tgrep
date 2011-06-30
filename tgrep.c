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
        int matchSize = (int)(matches[1].rm_eo - matches[1].rm_so) + 1;
        char match[matchSize];
        strncpy(match, timeString + (int)matches[1].rm_so, matchSize);
        regfree(&re);
        return atoi(match);
    }
    regfree(&re);
    return -1;
}

void printLineDate(lineDate* time)
{
    if(time->hour != -1)
    {
        printf("%i", time->hour);
        if(time->minute != -1)
        {
            printf(":%i", time->minute);
            if(time->second != -1)
            {
                printf(":%i", time->second);
            }
        }
        printf("\n");
    }
    else
    {
        printf("Bad date given\n");
    }
}

//only pass in single time as timeString
void populateLineDate(lineDate* time, char* timeString)
{
    char* hourPattern = "([0-9]{1,2}):";
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
    int secondTimeOffset;
    char* firstDate;
    char* secondDate;

    if(isRange(inputTimeString, &secondTimeOffset) != 0)
    {
        firstDate = malloc((strlen(inputTimeString) - secondTimeOffset) + 1);
        secondDate =  malloc(secondTimeOffset + 1);
        strcpy(firstDate, inputTimeString+secondTimeOffset);
        strncpy(secondDate, inputTimeString, --secondTimeOffset);
        secondDate[secondTimeOffset] = '\0';
        populateLineDate(myDate, firstDate);
        populateLineDate(myDate->secondDate, secondDate);
        printf("first: %s, second %s\n", firstDate, secondDate);
        free(secondDate);
    }
    else
    {
        firstDate = (char*) malloc(strlen(inputTimeString) + 1);
        strcpy(firstDate, inputTimeString);
        populateLineDate(myDate, firstDate);
        printf("first: %i\n", myDate->hour);
    }
    free(firstDate);
}

int lessThanDate(lineDate* search, lineDate* current)
{
    if(search->hour < current->hour)
    {
        return 1;
    }
    else if(search->hour == current->hour)
    {
        if(search->minute == -1 || search->minute < current->minute)
        {
            return 1;
        }
        else if(search->minute == current->minute)
        {
            if(search->second == -1 || search->second < current->second)
            {
                return 1;
            }
        }

    }

    return 0;
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
    lineDate date;
    lineDate readDate;
    lineDate secondDate;
    date.secondDate = &secondDate;
    char* filename;
    int errno;

    if(argc == 1)
    {
        printf("I need at least a timestamp to look for\n");
        return 1;
    }

    buildLineDate(&date, argv[1]);

    //first argument not a date
    if(date.hour == -1)
    {
        if(argc > 2)
        {
            filename = argv[1];
            buildLineDate(&date, argv[2]);
            if(date.hour == -1)
            {
                printf("Bad timestamp or no timestamp given.\n");
                return 1;
            }
        }
        else
        {
            printf("I need at least a timestamp to look for\n");
            return 1;
        }
    }
    else //first argument is a date
    {
        if(argc > 2)
        {
            filename = argv[2];
        }
        else
        {
            filename = "sample.log";
        }
    }

    FILE *file = fopen(filename, "r");

    if(file == NULL)
    {
        printf("Error opening file: ERRNO %i\n", errno);
    }

    char currentline[80];

    fgets(currentline, 80, file);

    printf("%s \n", currentline);
    buildLineDate(&readDate, currentline);
    printLineDate(&readDate);

    printf("%i \n", lessThanDate(&date, &readDate));

    return 0;
}


