#include <cs50.h>
#include <stdio.h>

int main(void)
{

    long num = get_long("Number: ");
    if ()
    {
        printf("AMEX\n");
    }
    else
    {
        printf("INVALID\n");
    }

}

int num_digits(long num)
{
    int count = 0;
    while (num != 0)
    {
        num /= 10;
        count += 1;
    }
    return count;
}
