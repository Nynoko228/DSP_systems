import math
import numpy as np
import pandas as pd
from scipy.stats import norm

m = 30

def read_fractions_from_file(filename):
    fractions = []
    with open(filename, 'r') as file:
        for line in file:
            value = float(".".join(line.strip().split(',')))
            fractions.append(value)
    return fractions

def array_splitting(array, m):
    b = math.ceil(len(array) / m)
    print(f"b равна: {b}")
    lst = []
    for i in range(m):
        lst.append(array[b*i:b*(i+1)])
    return b, lst

def f_calculation(array, m):
    f = []
    for i in range(m):
        f.append(sum(x**2 for x in array[i])/len(array[i]))
    print(f"np.median(f): {np.median(f)}")
    return f


def count_series(arr, f):
    """Функция для подсчёта количества серий (смен знака) в массиве"""
    signs = np.sign(arr - np.median(f))  # Определяем знаки относительно медианы
    return np.sum(signs[1:] != signs[:-1]) + 1 # Количество изменений знака


def calculate_confidence_bounds(n):
    """Вычисляем границы распределения для числа серий"""
    mean = (2 * n - 1) / 3
    std = np.sqrt((16 * n - 29) / 90)

    bounds_95 = (mean + norm.ppf(0.05) * std, mean + norm.ppf(0.95) * std)
    bounds_99 = (mean + norm.ppf(0.01) * std, mean + norm.ppf(0.99) * std)

    return bounds_95, bounds_99

def create_excel(filename, array, f):

    data = []
    cnt = 0
    for arr in array:
        arr = np.array(arr)
        b = len(arr)
        print(b)
        n_half = b / 2
        num_series = count_series(arr, f)
        (low_95, high_95), (low_99, high_99) = calculate_confidence_bounds(b)

        data.append([
            f"Array {cnt+1}", b, n_half, num_series, low_95, high_95, low_99, high_99
        ])
        cnt += 1

    # Создаём DataFrame
    columns = pd.MultiIndex.from_tuples([
        ("Имя", "", ""),
        ("b", "", ""),
        ("N/2", "", ""),
        ("Число серий", "", ""),
        ("Границы распределения числа серий", "α", "0.95"),
        ("Границы распределения числа серий", "α", "0.05"),
        ("Границы распределения числа серий", "α", "0.99"),
        ("Границы распределения числа серий", "α", "0.01")
    ])

    df = pd.DataFrame(data, columns=columns)

    # Сохраняем в Excel с объединением ячеек
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, index=True, merge_cells=True)  # merge_cells=True объединяет заголовки


if __name__ == "__main__":
    fractions = read_fractions_from_file("HL_Makh.txt")
    print(f"Количество элементов в файле: {len(fractions)}")
    b, lst = array_splitting(fractions, m)
    f = f_calculation(lst, m)
    create_excel("test.xlsx", lst, f)