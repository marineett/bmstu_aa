import matplotlib.pyplot as plt
import numpy as np

vertices = [3, 4, 5, 6, 7, 5, 7, 9, 10, 11]
brute_force_times = [0, 0, 1, 2, 2, 4.6, 7.5, 53, 200, 913]
ant_colony_times = [0, 1, 7, 7, 17, 4.9, 7.5, 20, 31, 32]

plt.figure(figsize=(10, 6))

plt.plot(vertices, ant_colony_times, label="Муравьиный алгоритм", color='blue', marker='o')
plt.plot(vertices, brute_force_times, label="Алгоритм полного перебора", color='red', marker='x')

plt.title("Сравнене алгоритмов по времени в зависимости от количества вершин")
plt.xlabel("Количество вершин графа")
plt.ylabel("Время выполнения (мс)")
plt.legend()

plt.grid(True)
plt.show()
