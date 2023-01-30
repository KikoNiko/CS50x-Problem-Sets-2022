#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

//Declare the functions before main
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //declare variables first
    string text;
    int letters, words, sentences, index;
    double L, S;

    //Ask the user for the text
    text = get_string("Text: ");

    //Call the necessary functions:
    letters = count_letters(text);
    words = count_words(text);
    sentences = count_sentences(text);

    //Link L and S to the letters and sentences per 100 words
    //words should be converted to floats, letters and sentences are ints and L, S should be doubles
    L = letters / (float)words * 100;
    S = sentences / (float)words * 100;

    //Implement formula and use round from math.h to round index to an int
    index = round(0.0588 * L - 0.296 * S - 15.8);

    //Extra conditions and final Output:
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}


//Count the letters inside the text
int count_letters(string text)
{
    int leng, counter = 0;
    leng = strlen(text);
    for (int i = 0; i < leng; i++)
    {
        if (isalpha(text[i]) != 0)
        {
            counter++;
        }
    }
    return counter;
}

//Count the words inside the text
int count_words(string text)
{
    int leng, counter = 0;
    leng = strlen(text);
    for (int i = 0; i < leng; i++)
    {
        if (text[i] == ' ')
        {
            counter++;
        }
    }
    counter++;
    return counter;
}

//Count the sentences of the text
int count_sentences(string text)
{
    int leng, counter = 0;
    leng = strlen(text);
    for (int i = 0; i < leng; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            counter++;
        }
    }
    return counter;
}