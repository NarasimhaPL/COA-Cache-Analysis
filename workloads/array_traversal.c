
#include <stdio.h>
#include <stdlib.h>

#define ARRAY_SIZE 1024

int main(void)
{
    int *array = malloc(ARRAY_SIZE * sizeof(int));

    if (array == NULL)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

    // Initialize the array.
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        array[i] = i;
    }

    // Sequentially read the array.
    long long sum = 0;

    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        sum += array[i];
    }

    printf("Array size: %d\n", ARRAY_SIZE);
    printf("Sum: %lld\n", sum);

    free(array);

    return 0;
}
