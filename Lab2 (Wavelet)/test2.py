import math
import scipy
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pywt
matplotlib.use('TkAgg')
def wavelet():
    # Входной сигнал
    # Пример использования:
    file_path = "HL_Makh.txt"  # Замените на ваш путь к файлу
    # file_path = "Data/4/ry.txt"  # Замените на ваш путь к файлу
    # file_path = "Data/4/triA.txt"  # Замените на ваш путь к файлу
    # file_path = "Data/4/y.txt"  # Замените на ваш путь к файлу
    with open(file_path, 'r') as f:
        # Читаем файл, заменяем запятые на точки и преобразуем в numpy массив
        signal = np.array([float(line.strip().replace(",", ".")) for line in f if line.strip()])


    # signal = np.array([6, 4, 13, 5, 9, 11, 13, 12, 10, 9, 4, 6, 13, 10, 8, 9])
    # cof = pywt.wavedec(signal, "haar", level=4)
    # print(cof[0])

    def haar_wavelet_transform(signal, levels):
        coeffs = []
        current_signal = signal.copy()
        print(f"levels: {levels}")
        for level in range(levels):
            n = (pow(2, math.floor(np.log2(len(current_signal)))))
            if n % 2 != 0:
                raise ValueError("Длина сигнала должна быть четной.")

            # Инициализация массивов для аппроксимаций и деталей
            approximation = np.zeros(n // 2)
            details = np.zeros(n // 2)

            # Вычисление аппроксимаций и деталей
            for i in range(n // 2):
                approximation[i] = (current_signal[2 * i] + current_signal[2 * i + 1]) / 2
                details[i] = (current_signal[2 * i] - current_signal[2 * i + 1]) / 2

            # Сохраняем коэффициенты
            coeffs.append((approximation, details))

            # Переходим к следующему уровню
            current_signal = approximation

        return coeffs

    # Выполняем вейвлет-преобразование
    # levels = math.floor(np.log2(len(signal)))  # Уровень разложения
    levels = 6  # Уровень разложения
    if levels > math.floor(np.log2(len(signal))):
        raise ValueError("Число уровней превышено.")
    coeffs = haar_wavelet_transform(signal, levels)
    energies = []
    # Выводим результаты
    for level, (approximation, details) in enumerate(coeffs):
        print(f"Уровень {level + 1}:")
        print("Аппроксимация (полусумма):", approximation)
        print("Детали (полуразности):", details)
        # energy_approximation = np.sum(np.square(approximation))
        # energy_details = np.sum(np.square(details))
        # total_energy = energy_approximation + energy_details
        # energies.append(total_energy)
        # print("energy_approx", energy_approximation)
        # print("energy_details", energy_details)

    # Визуализируем результаты
    plt.figure(figsize=(12, 8))
    fs = 2500

    for level, (approximation, details) in enumerate(coeffs):
        # time_approx = np.arange(len(approximation))  # Временные метки для аппроксимации
        # time_detail = np.arange(len(details))  # Временные метки для деталей
        time_approx = np.arange(len(approximation)) / fs * 1000
        time_detail = np.arange(len(details)) / fs * 1000
        plt.subplot(levels, 2, level * 2 + 1)
        plt.title(f'Уровень {level + 1} - Аппроксимация')
        # plt.plot(time_approx, approximation, marker=None)
        print(f"\n\n\n{approximation}")
        plt.step(time_approx, approximation, where='post', color='b', label='Прямоугольный сигнал')
        plt.grid()

        plt.subplot(levels, 2, level * 2 + 2)
        plt.title(f'Уровень {level + 1} - Детали')
        plt.step(time_detail, details, where='post', color='b', label='Прямоугольный сигнал')
        # plt.plot(time_detail, details, marker=None, color='orange')
        plt.grid()

    plt.tight_layout()
    plt.show()
    # print(np.sum(energies))
    # print(scipy.signal.welch(signal))


if __name__ == "__main__":
    print("entry point")
    wavelet()
