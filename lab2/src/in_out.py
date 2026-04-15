import matplotlib.pyplot as plt
from algs import create_random_matrix, insert_matrix
def input_matrix():
    print("Введите количество строк 1 матрицы")
    n1 = input()
    print("Введите количество стобцов 1 матрицы")
    m1 = input()
    print("Введите количество строк 2 матрицы")
    n2 = input()
    print("Введите количество столбцов 2 матрицы")
    m2 = input()

    if int(n1) <= 0 or int(m1) <= 0 or int(n2) <= 0 or int(m2) <= 0:
        print("Неверные размеры матриц")
        return
    print("Выберите вариант ввода матрицы")
    print("\t1. Ввести матрицу вручную \n"\
          "\t2. Сгенерировать случайную матрицу \n")
    choice = input()
    if choice == "1":
        return insert_matrix(int(n1), int(m1)), insert_matrix(int(n2), int(m2))
    elif choice == "2":
        return create_random_matrix(int(n1), int(m1)), create_random_matrix(int(n2), int(m2))
    else:
        print("Неверный вариант ввода матрицы")
        return
    
def check_input():
    print("\n  Меню  \n"
          "1) Классическое умножение матриц\n"
          "2) Умножение матриц по алгоритму Винограда\n"
          "3) Оптимизированный алгоритм Винограда\n"
          "4) Замеры времени\n"
          "0) Выход\n")
    return int(input("Выберите опцию: "))