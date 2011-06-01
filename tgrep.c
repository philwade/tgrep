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

//only pass in single time as timeString
int populateLineDate(lineDate* time, char* timeString)
{
    time->hour = 0;
    char *pattern = "([0-9]{1,2}):([0-9]{2}):([0-9]{2})|([0-9]{1,2}):([0-9]{2})";
    regex_t re;
    regmatch_t matches[4];
    int rangeOffset;

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
    lineDate* date;
    date = (lineDate*) malloc(sizeof(lineDate));

    char *test = "10";
    int test2 = atoi(test);
        printf("%i" , test2);

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
        printf("I need at least a timestamp to look for\n");
        return 1;
    }
    //printf("%i \n", date.hour);
    return 0;
}


