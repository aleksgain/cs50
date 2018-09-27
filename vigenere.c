#import <stdio.h>
#import <cs50.h>
#import <string.h>
#import <stdlib.h>
#import <ctype.h>

int main(int argc, string argv[])
{
    string keyword = argv[1];
    if (argc != 2)
    {
        printf("Give program a single keyword for cipher!\n");
        return 1;
    }
    else
    {
        int k = 0;
        int keys[strlen(keyword)];

        for (int i = 0; i < strlen(keyword); i++)
        {
            if (isalpha(keyword[i]) == 0)
            {
                printf("Give program a single keyword for cipher!\n");
                return 1;
            }
            else
            {
                keyword[i] = tolower(keyword[i]);
                keys[i] = ((int)keyword[i] - 97) % 26;
            }
        }
        string text = get_string("plaintext: ");

        for (int i = 0; i <= strlen(text); i++)
        {
            if (k == strlen(keyword))
            {
                k = 0;
            }
            if (isalpha(text[i]))
            {
                if (isupper(text[i]))
                {
                    text[i] = (((int)text[i] - 65 + keys[k]) % 26) + 65;
                    k++;
                }
                if (islower(text[i]))
                {
                    text[i] = (((int)text[i] - 97 + keys[k]) % 26) + 97;
                    k++;
                }
            }
        }
        printf("ciphertext: %s\n", text);
        return 0;
    }
}