#import <stdio.h>
#import <cs50.h>
#import <string.h>
#import <stdlib.h>
#import <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Give program a single numerical cipher!\n");
        return 1;
    }
    else
    {
        int cipher = atoi(argv[1]);
        string text = get_string("plaintext: ");
        for (int i = 0; i <= strlen(text); i++)
        {
            if (isalpha(text[i]))
            {
                if (isupper(text[i]))
                {
                    text[i] = (((int)text[i] - 65 + cipher) % 26) + 65;
                }
                if (islower(text[i]))
                {
                    text[i] = (((int)text[i] - 97 + cipher) % 26) + 97;
                }
            }
        }
        printf("ciphertext: %s\n", text);
    }
}