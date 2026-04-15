
import matplotlib.pyplot as plt
from time import process_time
from algs import multiply_base, multiply_win, multiply_win_op

def show_results(matrix_sizes, base_times, winograd_times, optimized_winograd_times):
    print("\nСравнение алгоритмов для различных размеров матриц\n")
    print(f"{'Размер':<10} | {'Классический':<20} | {'Виноград':<20} | {'Оптимизированный Виноград':<20}")
    print("-" * 80)

    for i in range(len(matrix_sizes)):
        print(f"{matrix_sizes[i]:<10} | {base_times[i]:<20.2e} | {winograd_times[i]:<20.2e} | {optimized_winograd_times[i]:<20.2e}")

def plot_results(matrix_sizes, base_times, winograd_times, optimized_winograd_times):
    plt.figure(figsize=(10, 7))

    plt.plot(matrix_sizes, base_times, label="Классический алгоритм", linestyle='-', marker='o', color='blue')

    plt.plot(matrix_sizes, winograd_times, label="Алгоритм Винограда", linestyle='--', marker='^', color='green')

    plt.plot(matrix_sizes, optimized_winograd_times, label="Оптимизированный Виноград", linestyle='-.', marker='s', color='red')

    plt.legend()
    plt.grid(True)
    plt.title("Сравнительный график времени выполнения алгоритмов на матрицах с четной размерностью")
    plt.xlabel("Размер матриц (строки и столбцы)")
    plt.ylabel("Время (секунды)")
    
    plt.show()

def time_function_execution(func, size):
    matrix1 = [[0] * size for _ in range(size)]
    matrix2 = [[0] * size for _ in range(size)]

    start = process_time()

    for _ in range(1):  
        func(matrix1, matrix2)

    end = process_time()

    return end - start 

def run_time_analysis(compare=False):
    times_classic = []
    times_winograd = []
    times_optimized_winograd = []

    matrix_sizes = [20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    for size in matrix_sizes:
        times_classic.append(time_function_execution(multiply_base, size))
        times_winograd.append(time_function_execution(multiply_win, size))
        times_optimized_winograd.append(time_function_execution(multiply_win_op, size))

    show_results(matrix_sizes, times_classic, times_winograd, times_optimized_winograd)
    plot_results(matrix_sizes, times_classic, times_winograd, times_optimized_winograd)

if __name__ == "__main__":
    run_time_analysis(compare=False)