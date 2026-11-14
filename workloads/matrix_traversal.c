
#include <stdio.h>

#define SIZE 64

int main(void)
{
    int matrix[SIZE][SIZE];
    long long sum = 0;

    // Initialize matrix
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            matrix[i][j] = i * SIZE + j;
        }
    }

    // Row-major traversal
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            sum += matrix[i][j];
        }
    }

    printf("Matrix size: %d x %d\n", SIZE, SIZE);
    printf("Sum: %lld\n", sum);

    return 0;
}
