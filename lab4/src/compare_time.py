import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("results.csv")

plt.figure(figsize=(10, 5))

unique_max_pages = data['MaxPages'].unique()

for max_pages in unique_max_pages:
    subset = data[data['MaxPages'] == max_pages]
    plt.plot(subset['Threads'], subset['ElapsedTime'], marker='o')

plt.title('Сравнение скорости парсинга относительно количества потоков')
plt.xlabel('Количество потоков')
plt.ylabel('Время (секунды)')

plt.xscale('log')
plt.xticks(data['Threads'].unique(), labels=[str(int(t)) for t in data['Threads'].unique()])

plt.legend()
plt.grid()

plt.savefig("parsing_comparison.png")

plt.show()
