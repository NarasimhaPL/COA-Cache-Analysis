
#include <stdio.h>
#include <stdlib.h>

#define ARRAY_SIZE 1024

int main(void)
{
    int array[ARRAY_SIZE];
    long long sum = 0;

    // Initialize array
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        array[i] = i;
    }

    // Generate a reproducible shuffled access order
    int indices[ARRAY_SIZE];

    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        indices[i] = i;
    }

    srand(42);

    for (int i = ARRAY_SIZE - 1; i > 0; i--)
    {
        int j = rand() % (i + 1);

        int temp = indices[i];
        indices[i] = indices[j];
        indices[j] = temp;
    }

    // Random-order array traversal
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        sum += array[indices[i]];
    }

    printf("Array size: %d\n", ARRAY_SIZE);
    printf("Sum: %lld\n", sum);

    return 0;
}
