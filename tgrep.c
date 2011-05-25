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
    char newTime[] = "10:10:10";

    buildLineDate(&date, newTime);
    printf("%i \n", date.hour);
    return 0;
}

int buildLineDate(lineDate* time, char timeString[])
{
    time->hour = 5;
    return 0;
}
