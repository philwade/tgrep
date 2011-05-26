#include <stdio.h>
#include <regex.h>

typedef struct line_date {
    int hour;
    int minute;
    int second;
} lineDate;

int main(void)
{
    lineDate date;
    char *pattern = "10:10:10111(1111)";
    regex_t re;
    regmatch_t matches[2];

    if(regcomp(&re, pattern, REG_EXTENDED) != 0)
    {
        printf("Failed to compile regex");
        return 1;
    }

    char *newTime = "10:10:101111111";

    if(regexec(&re, newTime, 2, matches, 0) != 0)
    {
        printf("Failed to match regex");
        return 1;
    }
    else
    {
        printf("%.*s", (int)(matches[1].rm_eo - matches[1].rm_so), &newTime[matches[1].rm_so]);
    }
    buildLineDate(&date, newTime);
    //printf("%i \n", date.hour);
    return 0;
}

int buildLineDate(lineDate* time, char timeString[])
{
    time->hour = 5;
    return 0;
}
