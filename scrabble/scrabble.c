#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}


int compute_score(string word)
{
    // TODO: Compute and return score for string
    //set a variable to keep the score
    int count_score = 0;
    //for loop starting from 0 to the end of the string word
    for (int i = 0; i < strlen(word); i++)
    {
        //check for lowercase and uppercase. Keep in mind in the ASCII Table A = 65, a = 97
        //calculate score by checking each letter in the string array asigning the POINTS accordingly and adding them to the count_score variable
        if (islower(word[i]))
        {
            count_score += POINTS[word[i] - 97];
        }
        else if (isupper(word[i]))
        {
            count_score += POINTS[word[i] - 65];
        }
    }
    return count_score;
}

