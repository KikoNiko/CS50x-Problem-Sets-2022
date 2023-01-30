// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned long N = 10000;

// Hash table
node *table[N];

// create a word counter
int word_counter = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // hash word to obtain a hash value
    unsigned int hash_value = hash(word); // unsigned int is for non negative values only

    // access linked list at that index in the hash table
    node *cursor = table[hash_value]; // this points to the head of the linked list

    // if word is in that list it is in dictionary
    // go through linked list looking one node at a time to look for word
    // cursor->next
    // Use strcasecmp to compare strings ignoring upper or lower case
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0) // strcasemp returns 0 if the strings are the same
        {
            return true;
        }

        cursor = cursor->next; // if strings dont match move cursor to next node
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // Take as input a word with alphabetical chars

    long value = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        value += toupper(word[i]);
    }

    // Output hash value number
    return value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open dictionary file - fopen
    FILE *file_ptr = fopen(dictionary, "r");
    if (file_ptr == NULL)
    {
        return false;
    }
    // Create an array for the words
    char next_word[LENGTH + 1]; //LENGTH + 1 to make sure we take into account the '\0'

    // Read strings from file one at a time - fscanf(file, "%s", word), fscanf will return EOF
    // while loop till the end of file
    while (fscanf(file_ptr, "%s", next_word) != EOF)
    {
        // Create a new node for each word - malloc (Check for NULL)
        node *n = malloc(sizeof(node));
        if (n != NULL)
        {
            // copy the word into the node using strcpy
            strcpy(n->word, next_word);

            // Hash word to obtain a hash value - use hash function
            unsigned int hash_value = hash(next_word);

            // Insert node into hash table at that location
            // index into the hash table to get to the linked list and add the word
            // creating new node set pointers in correct order adding the new node in the beggining of linked list
            n->next = table[hash_value];
            table[hash_value] = n;
            word_counter++;
        }
    }
    fclose(file_ptr);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // loop through hash table and free nodes on each link list
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
            temp = cursor;
        }
    }
    return true;
}
