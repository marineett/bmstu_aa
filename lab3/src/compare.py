import random
import time
import matplotlib.pyplot as plt
from main import normal_search, binary_search, merge_sort

def measure_search(arr, search_func, value):
    start_time = time.time()
    comparisons = search_func(arr, value)
    end_time = time.time()
    return comparisons, (end_time - start_time) * 1000 

def collect_compare(arr, search_func):
    comparison_data = []
    for i, value in enumerate(arr):
        comparisons, time_elapsed = measure_search(arr, search_func, value)
        comparison_data.append((i, comparisons, time_elapsed))
    return comparison_data

def plot_histogram(comparison_data, title, xlabel, ylabel, color, y_ticks):
    indices = [data[0] for data in comparison_data]
    comparisons = [data[1] for data in comparison_data]
    
    plt.figure(figsize=(10, 6))
    plt.bar(indices, comparisons, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.yticks(y_ticks)  
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

def main():
    length = 1000
    upper_bound = 1000
    arr = [random.randint(0, upper_bound) for _ in range(length)]
    search_value = random.choice(arr)

    linear_data = collect_compare(arr, normal_search)
    plot_histogram(linear_data, 
                   title="Число сравнений для поиска полным перебором",
                   xlabel="Индекс искомого элемента",
                   ylabel="Число сравнений",
                   color="green",
                   y_ticks=range(0, 1001, 200))
    
    merge_sort(arr, 0, len(arr) - 1)
    binary_data = collect_compare(arr, binary_search)
    sorted_binary_data = sorted(binary_data, key=lambda x: x[1])

    plot_histogram(sorted_binary_data, 
                   title="Число сравнений для бинарного поиска",
                   xlabel="Индекс искомого элемента (по числу сравнений)",
                   ylabel="Число сравнений",
                   color="blue",
                   y_ticks=range(0, 11, 2))

if __name__ == "__main__":
    main()