import math
import os

import numpy as np
import pandas as pd
from scipy.stats import norm
from openpyxl.workbook import Workbook

txt_files = ["HL_Makh.txt", "triA.txt", "y.txt"]


m = [20, 40]
a99 = [5, 13]
a95 = [6, 15]
a05 = [15, 26]
a01 = [16, 28]
a99i = [59, 290]
a95i = [69, 319]
a05i = [120, 460]
a01i = [130, 489]

def is_power_of_two(n):
    if n <= 0:
        return False
    log_value = math.log2(n)
    if log_value.is_integer():
        return n, 6 if log_value >= 6 else log_value
    power = 1
    while power * 2 < n:
        power *= 2
    return power, 6 if log_value >= 6 else log_value


def read_from_file(filename):
    lst = []
    cnt = 0
    with open(filename) as file:
        for line in file:
            cnt += 1
            lst.append(float(line.strip().replace(',', '.')))
    return lst, cnt

def schitaem_urovni(lvls, lst):
    razlojenie = {}
    n = len(lst)
    for i in range(lvls):
        for j in range(0, len(lst), 2):
            print(lst[j], lst[j+1])

def read_fractions_from_file(filename):
    fractions = []
    with open(filename, 'r') as file:
        for line in file:
            value = float(".".join(line.strip().split(',')))
            fractions.append(value)
    return fractions


def array_splitting(array, m):
    return np.array_split(array, m)
    # b = math.ceil(len(array) / m)
    # print(f"b равна: {b}")
    # lst = []
    # for i in range(m):
    #     lst.append(array[b*i:b*(i+1)])
    # return b, lst

def f_calculation(array, m):
    f = []
    ft = []
    for i in range(m):
        f.append(sum(x**2 for x in array[i])/len(array[i]))
        ft.append(np.sqrt(sum(x**2 for x in array[i])/len(array[i])))
    # print(f"np.median(f): {np.median(f)}")
    print(f"np.median(f): {np.median(ft)}")
    return ft


def count_series(arr, f):
    """Функция для подсчёта количества серий (смен знака) в массиве"""
    signs = np.sign(arr - np.median(f))  # Определяем знаки относительно медианы
    print(signs)
    print(f'\n{np.sum(signs[1:] != signs[:-1]) + 1}\n')
    return np.sum(signs[1:] != signs[:-1]) + 1 # Количество изменений знака

def count_inv(f, m):
    cnt = 0
    for i in range(m):
        print(f"{f[i]}", end=", ")
        for j in range(i + 1, m):
            print(f"{f[j]}", end=", ")
            if f[i] > f[j]:
                cnt += 1
    return cnt

def create_excel(filename, array, f, m, cnt, data, j):

    # arr = np.array(array)
    b = len(array[-1])
    # print(b)
    n_half = m / 2
    num_series = count_series(f, f)
    num_inv = count_inv(f, m)

    data.append([
        f"Сигнал {j}", b, n_half, m, num_series, num_inv, a95[cnt-1], a05[cnt-1], a99[cnt-1], a01[cnt-1], a95i[cnt-1], a05i[cnt-1], a99i[cnt-1], a01i[cnt-1]
    ])

    # Создаём DataFrame
    columns = pd.MultiIndex.from_tuples([
        ("Имя", "", ""),
        ("b", "", ""),
        ("N/2", "", ""),
        ("N", "", ""),
        ("Число серий", "", ""),
        ("Число инверсий", "", ""),
        ("Границы распределения числа серий", "α", "0.95"),
        ("Границы распределения числа серий", "α", "0.05"),
        ("Границы распределения числа серий", "α", "0.99"),
        ("Границы распределения числа серий", "α", "0.01"),
        ("Границы распределения числа инверсий", "α", "0.95"),
        ("Границы распределения числа инверсий", "α", "0.05"),
        ("Границы распределения числа инверсий", "α", "0.99"),
        ("Границы распределения числа инверсий", "α", "0.01")
    ])

    df = pd.DataFrame(data, columns=columns)

    # Проверяем, существует ли файл
    if os.path.exists(filename):
        # Если файл существует, открываем его
        with pd.ExcelWriter(filename, engine="openpyxl", mode='r+', if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=True, merge_cells=True)
    else:
        # Если файл не существует, создаем новый
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            df.to_excel(writer, index=True, merge_cells=True)


if __name__ == "__main__":
    data = []
    signal = np.array([6, 4, 13, 5, 9, 11, 13, 12, 10, 9, 4, 6, 13, 10, 8, 9])
    lvls = 4
    schitaem_urovni(lvls, signal)
    # for j in range(len(txt_files)):
    #     lst, cnt = read_from_file(txt_files[j])
    #     print(lst, cnt)
    #     cnt, L = is_power_of_two(cnt)
    #     print(L, cnt)
