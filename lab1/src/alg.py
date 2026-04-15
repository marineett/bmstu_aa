def create_matrix(n: int, m: int):
    matrix = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0:
                matrix[i][j] = j
            elif j == 0:
                matrix[i][j] = i
            else:
                matrix[i][j] = -1
    return matrix

def print_answer(lhs: str, rhs: str, matrix, verbose=True):
    if not verbose:
        return  
    
    print("   " + "  ".join(f"{ch}" for ch in rhs))  
    
    for i, row in enumerate(matrix):
        if i == 0:
            print("  " + " ".join(f"{val:2}" for val in row))  
        else:
            print(f"{lhs[i - 1]} " + " ".join(f"{val:2}" for val in row)) 

def levenstein_matrix(lhs: str, rhs: str, verbose=False):
    n = len(lhs)
    m = len(rhs)

    matrix = create_matrix(n + 1, m + 1)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            replace = matrix[i - 1][j - 1]
            if lhs[i - 1] != rhs[j - 1]:
                replace += 1
            insert = matrix[i - 1][j] + 1
            delete = matrix[i][j - 1] + 1
        
            matrix[i][j] = min(insert, delete, replace)

    if verbose:
        print_answer(lhs, rhs, matrix, verbose)  

    return matrix[-1][-1]

def levenstein_recursive(lhs: str, rhs: str, verbose=False):
    n = len(lhs)
    m = len(rhs)

    if verbose:
        print(f"Comparing '{lhs}' with '{rhs}'")

    if n == 0:
        return m
    if m == 0:
        return n

    replace = levenstein_recursive(lhs[:-1], rhs[:-1], verbose)  # Передайте verbose дальше
    
    if lhs[-1] != rhs[-1]:
        replace += 1

    insert = levenstein_recursive(lhs[:-1], rhs, verbose) + 1
    delete = levenstein_recursive(lhs, rhs[:-1], verbose) + 1

    return min(replace, insert, delete)


def levenstein_recursive_cash(lhs: str, rhs: str, matrix):
    n = len(lhs)
    m = len(rhs)
    if matrix[n][m] != -1:
        return matrix[n][m]
    
    replace = levenstein_recursive_cash(lhs[:-1], rhs[:-1], matrix)
    
    if (lhs[-1] != rhs[-1]):
        replace += 1

    insert = levenstein_recursive_cash(lhs[:-1], rhs, matrix) + 1
    delete = levenstein_recursive_cash(lhs, rhs[:-1], matrix) + 1

    matrix[n][m] = min(replace, insert, delete)
    return matrix[n][m] 

def levenstein_cash(lhs: str, rhs: str, verbose=False):
    n = len(lhs)
    m = len(rhs)
    matrix = create_matrix(n + 1, m + 1)
    if verbose:
        print(f"Computing Levenshtein distance for '{lhs}' and '{rhs}'")
    return levenstein_recursive_cash(lhs, rhs, matrix)  

def damerau_levenstein_matrix(lhs: str, rhs: str, verbose=False):
    n = len(lhs)
    m = len(rhs)

    matrix = create_matrix(n + 1, m + 1)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            replace = matrix[i - 1][j - 1]
            if lhs[i - 1] != rhs[j - 1]:
                replace += 1
            insert = matrix[i - 1][j] + 1
            delete = matrix[i][j - 1] + 1
            swap = float('inf')

            if i >= 2 and j >= 2:
                if lhs[i - 1] == rhs[j - 2] and lhs[i - 2] == rhs[j - 1]:
                    swap = matrix[i - 2][j - 2] + 1
            
            matrix[i][j] = min(insert, delete, replace, swap)

    if verbose:
        print_answer(lhs, rhs, matrix, verbose)  

    return matrix[-1][-1]

