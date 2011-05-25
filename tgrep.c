#include <stdio.h>

typedef struct line_date {
    int hour;
    int minute;
    int second;
} lineDate;

int main(void)
{
    lineDate date;
    buildLineDate(date);
    printf("%i", date.hour);
    char newTime[] = "10:10:10";
    return 0;
}

int buildLineDate(lineDate *time)
{
    time->hour = 5;
    return 0;
}
