#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);
    int n = height;
    for (int h = 0; h < height; h++)
    {
        for (int s = n - 1 ; s > 0; s--)
        {
            printf(" ");
        }
        for (int i1 = n - 1; i1 < height; i1++)
        {
            printf("#");
        }
        printf("  ");
        for (int i2 = n - 1; i2 < height; i2++)
        {
            printf("#");
        }
        printf("\n");
        n--;
    }
}
