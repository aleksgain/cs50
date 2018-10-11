// Implements a dictionary's functionality

#include <stdbool.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

int word_counter = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *words = root;
    for (int i = 0, x = strlen(word); i < x; i++)
    {
        //figure out the possible placement of element in trie
        int placement;
        if (word[i] == 39)
        {
            placement = 26;
        }
        else
        {
            placement = tolower(word[i]) - 97;
        }

        //check for element in trie. if empty, word failed the check, else dive further into trie.
        if (words->children[placement] == NULL)
        {
            return false;
        }
        else
        {
            words = words->children[placement];
        }
    }
    // upon the end of traversal check the is_word bool, return.
    if (words->is_word)
    {
        return true;
    }
    else
    {
        return false;
    }

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open file passed as dictionary
    FILE *file = fopen(dictionary, "r");

    //create a char for max length word
    char word[LENGTH + 1];

    //allocate a node for trie
    root = calloc(1, sizeof(node));
    node *dict = root;
    //iterate through dictionary
    while (fscanf(file, "%s", word) != EOF)
    {

        dict = root;

        //iterate through letters in each word
        for (int i = 0, x = strlen(word); i < x; i++)
        {
            //find a place to put the letter in the child trie
            int placement;
            if (word[i] == 39)
            {
                placement = 26;
            }
            else
            {
                placement = tolower(word[i]) - 97;
            }

            //allocate a node for new child if empty
            if (dict->children[placement] == NULL)
            {
                new_node = calloc(1, sizeof(node));
                dict->children[placement] = new_node;
            }

            dict = dict->children[placement];
        }

        dict->is_word = true;
        word_counter++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (!&load)
    {
        return 0;
    }
    else
    {
        return word_counter;
    }
}

// recursive function to unload children of node. Note: had to use calloc to preclear allocated memory, malloc would throw an error.
void recursiveUnload(node *cursor)
{
    for (int i = 0; i < 27; i++)
    {
        if (cursor->children[i])
        {
            recursiveUnload(cursor->children[i]);
        }
    }
    free(cursor);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{

    if (root)
    {
        recursiveUnload(root);
        return true;
    }
    else
    {
        return false;
    }

}
