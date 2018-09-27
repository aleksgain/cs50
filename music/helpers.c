// Helper functions for music

#include <cs50.h>
#include <string.h>
#include <math.h>
#include<stdio.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    //take first char out of fraction, convert to digit, do the same with the last char and multiply by 8
    int result = ((double)(fraction[0] - '0') / (double)(fraction[strlen(fraction) - 1] - '0')) * 8.0;
    return result;
}

// Calculates frequency (in Hz) of a note
int frequency(string n)
{
    //initialize the variables
    char note = n[0];
    double octave = n[strlen(n) - 1] - '0';
    double frequency = 440.0;
    double multiplier = octave - 4.0;
    double step = 0.0;
    char acc = '\0';

    //check for accidentals
    if (strlen(n) > 2)
    {
        acc = n[1];
    }

    //adjust for notes
    if (note == 'A')
    {
        step = 0.0;
    }
    else if (note == 'B')
    {
        step = 2.0;
    }
    else if (note == 'G')
    {
        step = -2.0;
    }
    else if (note == 'F')
    {
        step = -4.0;
    }
    else if (note == 'E')
    {
        step = -5.0;
    }
    else if (note == 'D')
    {
        step = -7.0;
    }
    else if (note == 'C')
    {
        step = -9.0;
    }

    //adjust for accidentals
    if (acc == '#')
    {
        step++;
    }
    else if (acc == 'b')
    {
        step--;
    }

    //calculate the frequency
    frequency = (frequency * pow(2.0, step / 12.0)) * pow(2.0, multiplier);

    return round(frequency);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (strcmp(s, "\n") == 0 || strcmp(s, "\r") == 0 || strcmp(s, "\r\n") == 0 || strcmp(s, "") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
