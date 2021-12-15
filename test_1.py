
"""
Написать программу, которая будет запускать процесс и с указанным интервалом времени собирать о нём следующую статистику:
1. Загрузка CPU (в процентах);
2. Потребление памяти: Working Set и Private Bytes (для Windows-систем)
или Resident Set Size и Virtual Memory Size (для Linux-систем);
3. Количество открытых хендлов (для Windows-систем) или файловых дескрипторов (для Linux-систем).
Сбор статистики должен осуществляться всё время работы запущенного процесса. Путь к файлу, который необходимо запустить,
и интервал сбора статистики должны указываться пользователем. Собранную статистику необходимо сохранить на диске.
Представление данных должно в дальнейшем позволять использовать эту статистику для автоматизированного построения
графиков потребления ресурсов.
"""

import os
import time
import psutil


cpu_list, handle_list, memory_used, memory_free = [], [], [], []
proc = psutil.Process()
current_process = psutil.Process()
total = ['CPU', 'Handle', 'Working Set Memory', 'Private Bytes Memory']
f_name = 'test_1.json'


num = 10     # количество секунд
path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\System Tools\Task Manager.lnk'     # путь к файлу


# функция получения id процесса
def get_pid(name):
    process_name = 'Taskmgr'
    pid = None
    for current_process in psutil.process_iter():
        if process_name in current_process.name():
            pid = current_process.pid
    return pid


p = psutil.Process(get_pid('Taskmgr'))


def test_1(num, path):
    os.startfile(path)
    while num > 0:
        print(f'осталось {num} секунд')
        time.sleep(1)                                               # снимаем статистику раз в секунду
        cpu = p.cpu_percent()
        handle = proc.open_files()

        wset = p.memory_info()
        private_bytes = p.memory_info()

        memory = psutil.virtual_memory()

        cpu_list.append(cpu)                                        # добавление загрузки CPU в процентах
        handle_list.append(len(handle))                             # добавление количества открытых хэндлов
        memory_used.append(wset[4] // 1024 ** 2)                    # добавление используемой памяти в МБ
        memory_free.append(private_bytes[-1] // 1024 ** 2)          # добавление свободной памяти в МБ

        num -= 1

    cpu_dict = dict(zip(list(range(1, len(cpu_list) + 1)), cpu_list))
    handle_dict = dict(zip(list(range(1, len(handle_list) + 1)), handle_list))
    used_memory_dict = dict(zip(list(range(1, len(memory_used) + 1)), memory_used))
    free_memory_dict = dict(zip(list(range(1, len(memory_free) + 1)), memory_free))

    stats_list = [cpu_dict, handle_dict, used_memory_dict, free_memory_dict]

    # преобразование статистики в словарь
    total_stats = dict(zip(total, stats_list))

    print(f'\nСтатистика успешно загружена в файл {f_name}')

    return total_stats


with open(f_name, 'w') as file:
    file.write(str(test_1(num, path)))



# вывод {'CPU': {1: 0.0, 2: 13.3, 3: 8.2, 4: 9.7, 5: 9.9, 6: 9.7, 7: 8.2, 8: 9.7, 9: 11.0, 10: 9.6}, 'Handle': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7, 9: 7, 10: 7}, 'Working Set Memory': {1: 27, 2: 28, 3: 28, 4: 28, 5: 28, 6: 28, 7: 28, 8: 28, 9: 28, 10: 28}, 'Private Bytes Memory': {1: 9, 2: 9, 3: 9, 4: 9, 5: 9, 6: 9, 7: 9, 8: 9, 9: 9, 10: 9}}