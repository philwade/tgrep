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

int main(int argc, char* argv[])
{
    lineDate date;
    char *pattern = "([0-9]{1,2}):([0-9]{2}):([0-9]{2})|([0-9]{1,2}):([0-9]{2})";
    regex_t re;
    regmatch_t matches[4];
    int rangeOffset;

    if(argc == 1)
    {
        printf("I need at least a timestamp to look for\n");
        return 1;
    }

    if(regcomp(&re, pattern, REG_EXTENDED) != 0)
    {
        printf("Failed to compile regex");
        return 1;
    }

    char *newTime = "10:11";

    if(regexec(&re, newTime, 4, matches, 0) != 0)
    {
        printf("Failed to match regex");
        return 1;
    }
    else
    {
        int i;
        for(i = 1;i < 4;i++)
        {
            printf("%.*s\n", (int)(matches[i].rm_eo - matches[i].rm_so), &newTime[matches[i].rm_so]);
        }
    }
    buildLineDate(&date, argv[1]);
    //printf("%i \n", date.hour);
    return 0;
}

int buildLineDate(lineDate* time, char* inputTimeString)
{
    int secondTimeOffset;
    char* firstDate;
    char* secondDate;

    if(isRange(inputTimeString, &secondTimeOffset) != 0)
    {
        firstDate = (char*) malloc(strlen(inputTimeString) - secondTimeOffset);
        secondDate = (char*) malloc(secondTimeOffset);
        strcpy(firstDate, inputTimeString+secondTimeOffset);
        strncpy(secondDate, inputTimeString, --secondTimeOffset);
        printf("first: %s, second %s\n", firstDate, secondDate);
    }
    else
    {
        //make sure we're a date at all
    }
    time;
    free(firstDate);
    free(secondDate);
    return 0;
}

lineDate parseDate(char* timeString)
{
    lineDate myDate;
    return myDate;
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
