#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // The program should take only one command-line argument
    // print error message and return 1
    if (argc != 2)
    {
        printf("Usage: ./recover 'filename'\n");
        return 1;
    }

    //Open memory card for reading
    FILE *memory_card = fopen(argv[1], "r");
    if (memory_card == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    //Define a buffer and count variable
    uint8_t buffer[BLOCK_SIZE];
    int counter = 0;
    //Create a pointer for location in memory to store the recovered images
    FILE *recovered_img = NULL;

    //Repeat until the end of memory card
    //Reads 512 bytes at a time into a buffer and stops if it doesn't return 512
    while (fread(buffer, 1, BLOCK_SIZE, memory_card) == BLOCK_SIZE)
    {
        //If file is a jpeg (checking first 4 bytes hexidecimal value)
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (counter == 0) //Check the first file first
            {
                //create new buffer to store new filenames in a string array of 8 bytes (because ###.jpg + '\0')
                //use sprintf function
                char new_filename[8];
                sprintf(new_filename, "%03i.jpg", counter);
                recovered_img = fopen(new_filename, "w");

                //Write the data from buffer into a new file. It should contain the recovered image
                fwrite(buffer, 1, BLOCK_SIZE, recovered_img);
            }

            if (counter > 0) //we create two separate conditions because we need to close the old file before writing to the new
            {
                char new_filename[8];
                sprintf(new_filename, "%03i.jpg", counter);

                fclose(recovered_img);
                recovered_img = fopen(new_filename, "w");

                fwrite(buffer, 1, BLOCK_SIZE, recovered_img);
            }

            counter++;
        }
        else
        {
            if (recovered_img != NULL)
            {
                //continue writing
                fwrite(buffer, 1, BLOCK_SIZE, recovered_img);
            }
        }

    }

    fclose(recovered_img);
    fclose(memory_card);
    return 0;
}