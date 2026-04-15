import random
import time

def calculate_length(X):
    if X // 8 + (X >> 2) % 10 == 0:
        return X % 1000
    else:
        return ((X >> 2) % 10 * (X % 10) + (X >> 1) % 10)

def normal_search(arr, value):
    for i in range(len(arr)):
        if arr[i] == value:
            return i
    return len(arr) 

def binary_search(arr, value):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == value:
            return mid
        elif arr[mid] < value:
            left = mid + 1
        else:
            right = mid - 1
    return len(arr)  

def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    left_part = arr[left:left + n1]
    right_part = arr[mid + 1:mid + 1 + n2]
    
    i = j = 0
    result = []
    while i < n1 and j < n2:
        if left_part[i] <= right_part[j]:
            result.append(left_part[i])
            i += 1
        else:
            result.append(right_part[j])
            j += 1

    result.extend(left_part[i:])
    result.extend(right_part[j:])
    
    for k in range(n1 + n2):
        arr[left + k] = result[k]

def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)

def main():
    X = int(input("Введите номер индивидуальной задачи: "))
    length = 10000
    upper_bound = 1000

    arr = [random.randint(0, upper_bound) for _ in range(length)]
    
    value1 = random.randint(0, upper_bound)
    start_time = time.time()
    index = normal_search(arr, value1)
    end_time = time.time()
    print(f"Результат линейного поиска: элемент {value1} находится на позиции {index} "
          f"(время выполнения: {end_time - start_time:.6f} секунд)")


    merge_sort(arr, 0, len(arr) - 1)

    start_time = time.time()
    index = binary_search(arr, arr[0])
    end_time = time.time()
    print(f"Результат бинарного поиска: элемент {arr[0]} (первый элемент отсортированного массива) "
          f"найден на позиции {index} (время выполнения: {end_time - start_time:.6f} секунд)")

if __name__ == "__main__":
    main()