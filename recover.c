#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover infile \n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];
    unsigned char buffer[512];
    char outfile[8];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // init output file
    FILE *outptr;

    // init search and file count values
    bool found = false;
    int count = 0;

    // start reading file 512 bytes at a time
    while (fread(buffer, 512, 1, inptr) == 1)
    {
        //check for beginning of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (!found)
            {
                found = true;
            }
            else
            {
                //close current file if new JPEG found
                fclose(outptr);
            }
            //open JPEG for append util new is found
            sprintf(outfile, "%03i.jpg", count);
            outptr = fopen(outfile, "a");
            count++;
        }

        if (found)
        {
            // write JPEG
            fwrite(&buffer, 512, 1, outptr);
        }
    }


    // close input and output files
    fclose(inptr);
    fclose(outptr);

    return 0;
}