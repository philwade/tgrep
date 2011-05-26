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
    char *pattern = "([0-9]{1,2}):([0-9]{2}):([0-9]{2})";
    regex_t re;
    regmatch_t matches[4];

    if(regcomp(&re, pattern, REG_EXTENDED) != 0)
    {
        printf("Failed to compile regex");
        return 1;
    }

    char *newTime = "10:11:12";

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
    buildLineDate(&date, newTime);
    //printf("%i \n", date.hour);
    return 0;
}

int buildLineDate(lineDate* time, char timeString[])
{
    time->hour = 5;
    return 0;
}
