import matplotlib.pyplot as plt

# Константы для названий алгоритмов
LEVENSHTEIN_MATRIX = "Нерекурсивный алгоритм нахождения расстояния Левенштейна"
LEVENSHTEIN_RECURSIVE_CACHE = "Рекурсивный алгоритм нахождения расстояния Левенштейна с кешированием"
LEVENSHTEIN_RECURSIVE = "Рекурсивный алгоритм нахождения расстояния Левенштейна"
DAMERAU_LEVENSHTEIN = "Нерекурсивный алгоритм нахождения расстояния Дамерау-Левенштейна"

def parse_algorithm_name(line):
    if line.startswith(LEVENSHTEIN_MATRIX):
        return 'levenshtein_matrix'
    elif line.startswith(LEVENSHTEIN_RECURSIVE_CACHE):
        return 'levenshtein_recursive_cache'
    elif line.startswith(LEVENSHTEIN_RECURSIVE):
        return 'levenshtein_recursive'
    elif line.startswith(DAMERAU_LEVENSHTEIN):
        return 'damerau_levenshtein'
    return None

def process_time_line(line, current_algorithm, times):
    parts = line.split()
    if len(parts) == 2:
        size, time = int(parts[0]), float(parts[1])
        if current_algorithm:
            times[current_algorithm]['sizes'].append(size)
            times[current_algorithm]['times'].append(time)

def read_execution_times(file_path):
    execution_times = {
        'levenshtein_matrix': {'sizes': [], 'times': []},
        'levenshtein_recursive_cache': {'sizes': [], 'times': []},
        'levenshtein_recursive': {'sizes': [], 'times': []},  
        'damerau_levenshtein': {'sizes': [], 'times': []}
    }
    current_algorithm = None
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            algorithm = parse_algorithm_name(line)
            if algorithm:
                current_algorithm = algorithm
            else:
                process_time_line(line, current_algorithm, execution_times)

    for alg, data in execution_times.items():
        print(f"{alg}: sizes={len(data['sizes'])}, times={len(data['times'])}")
    
    return execution_times

def create_comparison_graph(times):
    plt.figure(figsize=(10, 7))

    plt.plot(times['levenshtein_matrix']['sizes'], times['levenshtein_matrix']['times'], 
             label="Левенштейн (матрица)", color='blue', linestyle='-', marker='o')
    plt.plot(times['levenshtein_recursive_cache']['sizes'], times['levenshtein_recursive_cache']['times'], 
             label="Левенштейн (рекурсивный с кэшем)", color='orange', linestyle='--', marker='s')
    plt.plot(times['levenshtein_recursive']['sizes'], times['levenshtein_recursive']['times'], 
             label="Левенштейн (рекурсивный)", color='green', linestyle='-.', marker='^')  

    plt.legend()
    plt.grid(True)
    plt.title("Сравнительный анализ времени выполнения алгоритмов Левенштейна")
    plt.ylabel("Время (такты процессора)")
    plt.xlabel("Длина строки")
    plt.show()

def create_levenstein_vs_cache_graph(times):
    plt.figure(figsize=(10, 7))
    plt.plot(times['levenshtein_matrix']['sizes'], times['levenshtein_matrix']['times'], 
             label="Левенштейн (матрица)", linestyle='-', marker='D') 
    plt.plot(times['levenshtein_recursive_cache']['sizes'], times['levenshtein_recursive_cache']['times'], 
             label="Левенштейн (кеш)", linestyle='--', marker='v')  

    plt.legend()
    plt.grid(True)
    plt.title("Сравнение времени выполнения нерекурсивного Левенштейна и рекурсивного Левенштейна с кэшем")
    plt.ylabel("Время (такты процессора)")
    plt.xlabel("Длина строки")
    plt.show()

def create_matrix_vs_damerau_graph(times):
    plt.figure(figsize=(10, 7))
    plt.plot(times['levenshtein_matrix']['sizes'], times['levenshtein_matrix']['times'], 
             label="Левенштейн (матрица)", linestyle='-', marker='o')  
    plt.plot(times['damerau_levenshtein']['sizes'], times['damerau_levenshtein']['times'], 
             label="Дамерау-Левенштейн", linestyle='-.', marker='x')  
    
    plt.legend()
    plt.grid(True)
    plt.title("Сравнение времени выполнения нерекурсивного Левенштейна и нерекурсивного Дамерау-Левенштейна")
    plt.ylabel("Время (такты процессора)")
    plt.xlabel("Длина строки")
    plt.show()

def main():
    print("\nЧтение данных для графика 1:")
    execution_times1 = read_execution_times('/Users/marina/Desktop/5sem/AA/pmi22u275/src/all_1.txt')
    create_comparison_graph(execution_times1)

    print("\nЧтение данных для графика 2:")
    execution_times2 = read_execution_times('/Users/marina/Desktop/5sem/AA/pmi22u275/src/lev_2.txt')
    create_levenstein_vs_cache_graph(execution_times2)

    print("\nЧтение данных для графика 3:")
    execution_times3 = read_execution_times('/Users/marina/Desktop/5sem/AA/pmi22u275/src/lev_d_3.txt')
    create_matrix_vs_damerau_graph(execution_times3)

if __name__ == "__main__":
    main()
