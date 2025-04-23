import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import variation
from openpyxl.workbook import Workbook

# triA.txt и y.txt 8000 Гц, а у HL_Makh.txt 10000 Гц
txt_files = {"HL_Makh.txt": 10000, "triA.txt": 8000, "y.txt": 8000}
txt_files = {"TestLab4GE.txt": 10000}

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
    """Локальный спектр энергии в скользящем окне"""
    n = len(coeffs)
    return [np.sum(coeffs[i:i+window_size]**2) for i in range(0, n, window_size)]

def global_energy_spectrum(approx_energy, detail_energy):
    """Глобальный спектр энергии для всех уровней"""
    return {level: approx_energy[level] + detail_energy[level] for level in approx_energy}

def calculate_intermittency(coeffs):
    """Мера перемежаемости через коэффициент вариации"""
    return variation(np.abs(coeffs))

def calculate_contrast(approx_energy, detail_energy):
    """Контраст как отношение энергии деталей к аппроксимации"""
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
    approx = {i: [] for i in range(lvls)}
    details = {i: [] for i in range(lvls)}
    energy = {"approx": {}, "details": {}}

    plotnost = {"approx": {i: [] for i in range(lvls)}, "details": {i: [] for i in range(lvls)}}
    current_signal = lst
    for level in range(lvls):
        approx_coeffs = []
        detail_coeffs = []
        new_lst = []
        for j in range(0, len(lst), 2):
            approx[level].append((lst[j] + lst[j + 1]) / 2)
            new_lst.append((lst[j] + lst[j + 1]) / 2)
            details[level].append((lst[j] - lst[j + 1]) / 2)
        # np.sum(np.square(approx[i]))
        plotnost["approx"][level].append(np.sum(np.square(approx[level])))
        plotnost["details"][level].append(np.sum(np.square(details[level])))
        lst = new_lst
    # print(approx)
    # print(details)
    return approx, details, plotnost


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
    data = []
    for i in txt_files:
        print(i)
        print(txt_files[i])
        signal, cnt = read_from_file(i)
        N, L = is_power_of_two(cnt)
        print(L, N)
        approximation, details, energy = schitaem_urovni(L, signal[:N])
        features = {
            ""
        }
        for j in energy:
            if j == "approx":
                print("Аппроксимация: ", end='')
            else:
                print("Детали: ", end='')
            for k in energy[j]:
                print(f"уровень: {k}, плотность: {float(energy[j][k][0])}", end=' ')
            print()
