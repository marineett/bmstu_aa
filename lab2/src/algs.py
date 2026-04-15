import random

def insert_matrix(n: int, m: int):
    matrix = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            matrix[i][j] = int(input())
    return matrix


def create_random_matrix(n: int, m: int):
    matrix = [[random.randint(0, 100) for _ in range(m)] for _ in range(n)]  
    return matrix


def print_answer(matrix, verbose=True):
    if not verbose:
        return  
    
    for i, row in enumerate(matrix):
        print("  " + " ".join(f"{val:2}" for val in row)) 
        

def multiply_base(matrix1, matrix2):
    n1 = len(matrix1)
    m1 = len(matrix1[0])
    n2 = len(matrix2)
    m2 = len(matrix2[0])

    if m1 != n2:
        print("Wrong sizes.")
        return []
    
    res = [[0] * m2 for _ in range(n1)]

    for i in range(n1):
        for j in range(m2):
            for u in range(m1):
                res[i][j] += matrix1[i][u] * matrix2[u][j]
    
    return res

def multiply_win(matrix1, matrix2):

    n1 = len(matrix1)
    m1 = len(matrix1[0])
    n2 = len(matrix2)
    m2 = len(matrix2[0])

    if m1 != n2:
        print("Wrong sizes.")
        return []
    
    res = [[0] * m2 for _ in range(n1)]

    mult1 = [0] * n1
    for j in range(m1 // 2):
        mult1[0] += matrix1[0][j * 2] * matrix1[0][(j * 2) + 1]
    for i in range(1, n1, 1):
        for j in range(m1 // 2):
            mult1[i] += matrix1[i][j * 2] * matrix1[i][(j * 2) + 1]
    
    mult2 = [0] * m2
    for i in range(n2 // 2):
        mult2[0] += matrix2[i * 2][0] * matrix2[(i * 2) + 1][0]
    for j in range(1, m2, 1):
        for i in range(n2 // 2):
            mult2[j] += matrix2[i * 2][j] * matrix2[(i * 2) + 1][j]


    for j in range(m2):
        res[0][j] = mult1[0] - mult2[j]

        for u in range(m1 // 2):
            res[0][j] += (matrix1[0][(u * 2) + 1] + matrix2[u][j]) * \
                                  (matrix1[0][u * 2] + matrix2[u + 1][j])
    for i in range (1, n1, 1):
        for j in range(m2):
            res[i][j] = mult1[i] - mult2[j]
            for u in range(m1 // 2):
                res[i][j] += (matrix1[i][(u * 2) + 1] + matrix2[u][j]) * \
                                  (matrix1[i][u * 2] + matrix2[u + 1][j])

    if m1 % 2 == 1:
        for j in range(m2):
            res[0][j] += matrix1[0][m1 - 1] * matrix2[m1 - 1][j]
        for i in range(1, n1, 1):
            for j in range(m2):
                res[i][j] += matrix1[i][m1 - 1] * matrix2[m1 - 1][j]
    return res

def multiply_win_op(matrix1, matrix2):

    n1 = len(matrix1)
    m1 = len(matrix1[0])
    n2 = len(matrix2)
    m2 = len(matrix2[0])

    if m1 != n2:
        print("Wrong sizes.")
        return []
    
    res = [[0] * m2 for _ in range(n1)]

    mult1 = [0] * n1
    for j in range(m1 >> 1):
        mult1[0] += matrix1[0][j << 1] * matrix1[0][(j << 1) + 1]
    for i in range(1, n1, 1):
        for j in range(m1 >> 1):
            mult1[i] += matrix1[i][j << 1] * matrix1[i][(j << 1) + 1]
            
    mult2 = [0] * m2
    for i in range(n2 >> 1):
        mult2[0] += matrix2[i << 1][0] * matrix2[(i << 1) + 1][0]
    for j in range(1, m2, 1):
        for i in range(n2 >> 1):
            mult2[j] += matrix2[i << 1][j] * matrix2[(i << 1) + 1][j]


    for j in range(m2):
        res[0][j] = mult1[0] - mult2[j]

        for u in range(m1 >> 1):
            res[0][j] += (matrix1[0][(u << 1) + 1] + matrix2[u][j]) * \
                                  (matrix1[0][u << 1] + matrix2[u + 1][j])
    for i in range (1, n1, 1):
        for j in range(m2):
            res[i][j] = mult1[i] - mult2[j]

            for u in range(m1 >> 1):
                res[i][j] += (matrix1[i][(u << 1) + 1] + matrix2[u][j]) * \
                                  (matrix1[i][u << 1] + matrix2[u + 1][j])

    if m1 % 2 == 1:
        for j in range(m2):
            res[0][j] += matrix1[0][m1 - 1] * matrix2[m1 - 1][j]
        for i in range(1, n1, 1):
            for j in range(m2):
                res[i][j] += matrix1[i][m1 - 1] * matrix2[m1 - 1][j]
    return res