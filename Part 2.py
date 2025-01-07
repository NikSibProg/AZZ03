import numpy as np
import matplotlib.pyplot as plt

# Генерация случайных данных
num_samples = 100  # Количество точек
x_data = np.random.rand(num_samples)  # Набор случайных чисел для оси X
y_data = np.random.rand(num_samples)  # Набор случайных чисел для оси Y

# Построение диаграммы рассеяния
plt.figure(figsize=(8, 6))
plt.scatter(x_data, y_data, color='blue', alpha=0.6, edgecolor='black')
plt.title('Диаграмма рассеяния для случайных данных')
plt.xlabel('X - данные')
plt.ylabel('Y - данные')
plt.grid(True)
plt.show()
