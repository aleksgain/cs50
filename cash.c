#import <stdio.h>
#import <cs50.h>
#import <math.h>

int main(void)
{
    float change_input;
    int change;
    int counter = 0;
    do
    {
        change_input = get_float("Change owed: ");
    }
    while (change_input < 0.009);
    change = round(change_input * 100);
    while (change > 0)
    {
        if (change - 25 >= 0)
        {
            change = change - 25;
            counter++;
        }
        else if (change - 10 >= 0)
        {
            change = change - 10;
            counter ++;
        }
        else if (change - 5 >= 0)
        {
            change = change - 5;
            counter ++;
        }
        else if (change - 1 >= 0)
        {
            change = change - 1;
            counter ++;
        }
    }
    printf("%i\n", counter);
}

