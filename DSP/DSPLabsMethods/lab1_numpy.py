import numpy as np


def split_blocks(file_path, num_blocks):
    """
    Считывает числа из текстового файла, заменяет запятые на точки, разбивает их на заданное
    количество блоков (num_blocks), вычисляет размер блока, вычисляет среднее квадратичное
    значение для каждого блока, подсчитывает серии блоков, расположенных по одну сторону
    от медианы среднего квадратичного значения, подсчитывает число инверсий и возвращает
    список блоков, общее количество чисел, количество блоков, размер блока, средние
    квадратичные значения, количество серий и общее число инверсий.

    Аргументы:
        file_path (str): Путь к текстовому файлу с числами.
        num_blocks (int): Желаемое количество блоков.

    Возвращает:
        tuple: Кортеж, содержащий:
            - list: Список блоков, где каждый блок - это массив numpy.
            - int: Общее количество чисел, считанных из файла.
            - int: Общее количество блоков, созданных.
            - int: Размер блока.
            - list: Список средних квадратичных значений для каждого блока.
            - int:  Общее количество серий блоков, расположенных по одну сторону от медианы.
            - int: Общее количество инверсий.
        Возвращает ([], 0, 0, 0, [], 0, 0), если файл не существует или не содержит чисел.
        Если количество чисел меньше, чем num_blocks, возвращает только один блок
        со всеми числами.
    """

    try:
        with open(file_path, 'r') as f:
            # Читаем файл, заменяем запятые на точки и преобразуем в numpy массив
            numbers = np.array([float(line.strip().replace(",", ".")) for line in f if line.strip()])

        num_count = len(numbers)  # Вычисляем общее количество чисел

        if num_count < num_blocks:
            blocks = [numbers]  # Если чисел меньше, чем запрошено блоков, создаем только один блок
            block_size = num_count
            num_blocks = 1  # корректируем количество блоков
        else:
            block_size = num_count // num_blocks  # Определяем размер блока
            blocks = np.array_split(numbers, num_blocks)  # Разбиваем массив на блоки

        block_count = len(blocks)

        # Вычисляем средние квадратичные значения для каждого блока
        rms_values = [np.sqrt(np.mean(block ** 2)) for block in blocks]

        # Подсчет серий блоков, расположенных по одну сторону от медианы
        series_count = 0
        if block_count > 0:
            median = np.median(rms_values)  # Вычисляем медиану средних квадратичных значений
            print(f"MEDIAN: {median}")
            series_count = 1
            current_side = 1 if rms_values[0] >= median else -1  # 1: больше или равно медиане, -1: меньше медианы

            for i in range(1, block_count):
                side = 1 if rms_values[i] >= median else -1
                if side != current_side:
                    series_count += 1
                    current_side = side

        # Подсчет инверсий
        inversion_count = 0
        for i in range(block_count):
            for j in range(i + 1, block_count):
                if rms_values[i] > rms_values[j]:
                    inversion_count += 1

        return blocks, num_count, block_count, block_size, rms_values, series_count, inversion_count

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return [], 0, 0, 0, [], 0, 0
    except ValueError:
        print(f"Ошибка: Файл '{file_path}' содержит некорректные данные (не числовые значения).")
        return [], 0, 0, 0, [], 0, 0
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return [], 0, 0, 0, [], 0, 0


if __name__ == "__main__":
    print("entry point")

    # Пример использования:
    file_path = "HL_Makh.txt"  # Замените на ваш путь к файлу
    # file_path = "Data/4/ry.txt"  # Замените на ваш путь к файлу
    # file_path = "Data/4/triA.txt"  # Замените на ваш путь к файлу
    # file_path = "Data/4/y.txt"  # Замените на ваш путь к файлу
    num_blocks = 40  # Задаем желаемое количество блоков

    blocks, num_count, block_count, block_size, rms_values, series_count, inversion_count = split_blocks(file_path,
                                                                                                         num_blocks)

    if blocks:  # Проверяем, что блоки были успешно созданы
        print("Блоки чисел:")
        for i, block in enumerate(blocks):
            print(f"Блок {i + 1}: {block}, Среднее квадратичное: {rms_values[i]}")

        print(f"\nВсего чисел: {num_count}")
        print(f"Всего блоков: {block_count}")
        print(f"Размер блока: {block_size}")  # Вывод размера блока
        print(f"Всего серий (относительно медианы): {series_count}")
        print(f"Всего инверсий: {inversion_count}")
