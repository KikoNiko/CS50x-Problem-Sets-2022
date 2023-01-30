#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string s);
char rotate(char p, int k);

int main(int argc, string argv[])
{
    // Check for one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Check if argv[1] is a number
    if (!only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        printf("Key must be an integer!\n");
        return 1;
    }

    // Convert string to an int
    int k = atoi(argv[1]);
    // Ask user for plaintext
    string plaintext = get_string("plaintext:  ");

    // store the lenght of plaintext in a var L for cleaner code
    int L = strlen(plaintext);
    // store cipher text in an array of chars with lenght of L + 1 to include the null character
    // the null character indicates the end of a string
    char ciphertext[L + 1];

    // For each character in plaintext rotate it using the rotate function
    for (int i = 0; i < L; i++)
    {
        ciphertext[i] = rotate(plaintext[i], k);
    }

    // set the end of the string
    ciphertext[L] = '\0';
    // Output the ciphertext
    printf("ciphertext: %s", ciphertext);
    printf("\n");

    return 0;
}

// this function checks if chars in a string are digits
bool only_digits(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        // isdigit returns 0 if char is not a digit
        if (isdigit(s[i]) == 0)
        {
            return false;
        }
    }
    return true;
}

// rotate function takes a char and converts it to another char using a key
// rotate formula is c = (p + k) % 26
// c is rotated cipher character, p is original character
char rotate(char p, int k)
{
    char c;
    // check if char is alphabetical and then the case
    // we have to subtract the ascci value of 'a' or 'A' from char if its lower or upper case
    // and add it again at the end to get the right cipher char
    if (isalpha(p))
    {
        if (islower(p) != 0)
        {
            c = ((p - 97 + k) % 26) + 97;
        }
        else
        {
            c = ((p - 65 + k) % 26) + 65;
        }
    }
    else
    {
        return p;
    }

    return c;
}