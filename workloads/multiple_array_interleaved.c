
#include <stdio.h>

#define ARRAY_SIZE 64

int main(void)
{
    int A[ARRAY_SIZE];
    int B[ARRAY_SIZE];
    int C[ARRAY_SIZE];

    long long sum = 0;

    // Initialize all three arrays
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        A[i] = i;
        B[i] = i + 100;
        C[i] = i + 200;
    }

    // Interleaved access
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        sum += A[i];
        sum += B[i];
        sum += C[i];
    }

    printf("Array size: %d\n", ARRAY_SIZE);
    printf("Number of arrays: 3\n");
    printf("Sum: %lld\n", sum);

    return 0;
}
