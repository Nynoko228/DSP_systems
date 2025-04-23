import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import variation
from openpyxl.workbook import Workbook

# triA.txt и y.txt 8000 Гц, а у HL_Makh.txt 10000 Гц
# txt_files = {"HL_Makh.txt": 10000, "triA.txt": 8000, "y.txt": 8000}
# txt_files = {"TestLab4GE.txt": 10000}
txt_files = ["Bad\\B12.txt", "Bad\\B13.txt", "Bad\\B61.txt", "Bad\\B63.txt", "Neob2\\N11.txt", "Neob2\\N21.txt",
             "Neob2\\N31.txt", "Neob2\\N36.txt"]

m = [20, 40]
a99 = [5, 13]
a95 = [6, 15]
a05 = [15, 26]
a01 = [16, 28]
a99i = [59, 290]
a95i = [69, 319]
a05i = [120, 460]
a01i = [130, 489]


def local_energy_spectrum(coeffs, window_size=10):
    coeffs_array = np.array(coeffs)
    n = len(coeffs_array)
    return [float(np.sum(coeffs_array[i:i+window_size]**2)) for i in range(0, n, window_size)]

def global_energy_spectrum(approx_energy, detail_energy):
    return {level: approx_energy[level] + detail_energy[level] for level in approx_energy}

def calculate_intermittency(coeffs):
    return variation(np.abs(coeffs))

def calculate_contrast(approx_energy, detail_energy):
    return {level: detail_energy[level]/approx_energy[level] if approx_energy[level] != 0 else 0
            for level in approx_energy}

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
    approx = {}
    details = {}
    energies = {"approx": {}, "details": {}}

    current_signal = lst.copy()
    for level in range(lvls):
        if len(current_signal) < 2:
            break  # Прекращаем, если сигнал слишком короткий

        approx_coeffs = []
        detail_coeffs = []
        for j in range(0, len(current_signal) - 1, 2):
            avg = (current_signal[j] + current_signal[j + 1]) / 2
            diff = (current_signal[j] - current_signal[j + 1]) / 2
            approx_coeffs.append(avg)
            detail_coeffs.append(diff)


        approx[level] = approx_coeffs
        details[level] = detail_coeffs
        energies["approx"][level] = np.sum(np.square(approx_coeffs))
        energies["details"][level] = np.sum(np.square(detail_coeffs))
        current_signal = approx_coeffs  # Обновляем сигнал для следующего уровня

    return approx, details, energies


def read_fractions_from_file(filename):
    fractions = []
    with open(filename, 'r') as file:
        for line in file:
            value = float(".".join(line.strip().split(',')))
            fractions.append(value)
    return fractions


def array_splitting(array, m):
    return np.array_split(array, m)


def count_series(arr, f):
    """Функция для подсчёта количества серий (смен знака) в массиве"""
    signs = np.sign(arr - np.median(f))  # Определяем знаки относительно медианы
    print(signs)
    print(f'\n{np.sum(signs[1:] != signs[:-1]) + 1}\n')
    return np.sum(signs[1:] != signs[:-1]) + 1  # Количество изменений знака


if __name__ == "__main__":
    results = []
    # for filename, freq in txt_files.items():
    for filename in txt_files:
        print(f"filename: {filename}")
        plt.figure(figsize=(12, 8))
        lst, cnt = read_from_file(filename)
        N, L = is_power_of_two(cnt)
        print(L, N)
        approximation, details, energy = schitaem_urovni(L, lst[:N])
        print(energy)
        features = {
            "Локальная энергия": {level: local_energy_spectrum(details[level])
                                  for level in details},
            "Глобальная энергия": global_energy_spectrum(energy["approx"], energy["details"]),
            "Перемежаемость": {level: calculate_intermittency(details[level])
                               for level in details},
            "Контраст": calculate_contrast(energy["approx"], energy["details"])
        }

        # Сохранение в Excel
        with pd.ExcelWriter(f"{filename}_analysis.xlsx") as writer:
            for level in approximation:
                pd.DataFrame({
                    "Аппроксимация": approximation[level],
                    "Детали": details[level]
                }).to_excel(writer, sheet_name=f"Уровень {level}")

            pd.DataFrame(features).to_excel(writer, sheet_name="Характеристики")

        results.append(features)


