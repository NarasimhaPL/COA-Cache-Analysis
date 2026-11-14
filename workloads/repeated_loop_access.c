
#include <stdio.h>

#define ARRAY_SIZE 64
#define REPETITIONS 100

int main(void)
{
    int array[ARRAY_SIZE];
    long long sum = 0;

    // Initialize array
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        array[i] = i;
    }

    // Repeatedly access the same array
    for (int repeat = 0; repeat < REPETITIONS; repeat++)
    {
        for (int i = 0; i < ARRAY_SIZE; i++)
        {
            sum += array[i];
        }
    }

    printf("Array size: %d\n", ARRAY_SIZE);
    printf("Repetitions: %d\n", REPETITIONS);
    printf("Sum: %lld\n", sum);

    return 0;
}
