import numpy as np

def haar_wavelet_decomposition(signal, levels):
    """
    Выполняет вейвлет-разложение сигнала с использованием вейвлета Хаара.

    :param signal: Входной сигнал (numpy массив), длина которого является степенью 2.
    :param levels: Количество уровней разложения.
    :return: Словарь с коэффициентами вейвлет-разложения для каждого уровня.
    """
    if len(signal) == 0 or (len(signal) & (len(signal) - 1)) != 0:
        raise ValueError("Длина сигнала должна быть ненулевой и равной степени 2.")

    coeffs = {}
    current_signal = signal.copy()

    for level in range(levels):
        n = len(current_signal)
        # Создаем массив для хранения средних и разностей
        averages = np.zeros(n // 2)
        differences = np.zeros(n // 2)


        for i in range(0, n, 2):
            print(current_signal[i], current_signal[i + 1])
            averages[i // 2] = (current_signal[i] + current_signal[i + 1]) / 2
            differences[i // 2] = (current_signal[i] - current_signal[i + 1]) / 2

        coeffs[level] = differences  # Сохраняем разности (высокочастотные коэффициенты) в словарь
        current_signal = averages  # Переходим к средним (низкочастотные коэффициенты)

    coeffs[levels] = current_signal  # Сохраняем последние низкочастотные коэффициенты в словарь
    return coeffs

# Пример использования
if __name__ == "__main__":
    # Пример сигнала (длина 8, что является степенью 2)
    signal = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    levels = 2

    coeffs = haar_wavelet_decomposition(signal, levels)
    print("Коэффициенты вейвлет-разложения:")
    for level, coeff in coeffs.items():
        print(f"Уровень {level}: {coeff}")