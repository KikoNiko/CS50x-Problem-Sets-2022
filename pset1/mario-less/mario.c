#include <cs50.h>
#include <stdio.h>

int main(void)
{
//Prompt the user for Height until they input a number between 1 and 8.
  int height;
  do
  {
    height = get_int("Height: ");
  }
  while (height < 1 || height > 8);
//Check condition starting from 1 through height for each row using for loop.
for (int i = 0; i < height; i++)
{
    //to make a reverse pyramid we need spaces for each row equal to height - row - 1
    for (int x = 0; x < height - i - 1; x++)
    {
        //print spaces
        printf(" ");
    }
    //then we check condition for the columns and print hashtags
        for (int j = 0; j <= i; j++)
        {
            //print hashes
            printf("#");
        }
    //Create a new line after each cycle to make the rows.
        printf("\n");
    }
}
