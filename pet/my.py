#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

# import module
from tabulate import tabulate

import datetime
import sys
import pickle


def new_week(n_list):
    """
    Создание новой еженедельной задачи
    """
    # Запросить данные о человеке.
    day = input("На какой день добавить задачу? "
                "(пн, вт ...)  ").lower()
    if day in n_list:
        task = input("Введите задачу: ")
        n_list[day].append(task)
        print("Запись добавлена, воспользуйтесь 'list', "
              "чтоб посмотреть изменения")
    else:
        print("Некорректный день недели")
        new_week(n_list)


def new_task():
    """
    Создание новой однодневной задачи
    """
    d_date = list(map(int, input("Дата (дд.мм.гггг): ").split('.')))
    date = datetime.date(d_date[2], d_date[1], d_date[0])
    content = input("Введите задачу: ")
    # Создать словарь.
    return {
        'content': content,
        'date': date
    }


def display_list(s):
    """
    Вывод содержания списка задач
    """
    if s:
        print(tabulate(s, headers='keys'))

    else:
        print("Задач нет)")


def del_week(my_todo_list):
    """
    Удалить еженедельную задачу
    """
    day = input("Введите день недели (пн, вт, ...): ")
    if day in my_todo_list:
        task = input("Введите задачу: ")
        for d, t in my_todo_list.items():
            if d == day:
                t.remove(task)
                print("Запись удалена")
    else:
        print("Некорректный день недели")
        del_week(my_todo_list)


def del_task(tasks):
    """
    Удалить однодневную задачу
    """
    task = input("Введите задачу: ")
    flag = 0
    for i, item in enumerate(tasks):
        if item['content'] == task:
            tasks.pop(i)
            print("Запись удалена")
            flag = 1
            break
    if flag == 0:
        print("Запись не найдена")


def upd(tasks, week):
    """
    Обновить списки
    """
    with open('list_t.data', 'rb') as my_file1:
        # сохраняем данные как двоичный поток
        tasks = pickle.load(my_file1)
    with open('list_w.data', 'rb') as my_file2:
        # сохраняем данные как двоичный поток
        week = pickle.load(my_file2)
    return tasks, week


def cls():
    """
    Очистить консоль
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def save(tasks, my_todo_list):
    """
    Сохранить изменения
    """
    with open('list_t.data', 'wb') as my_file1:
        # сохраняем данные как двоичный поток
        pickle.dump(tasks, my_file1)
    with open('list_w.data', 'wb') as my_file2:
        # сохраняем данные как двоичный поток
        pickle.dump(my_todo_list, my_file2)
    print("Изменения сохранены")


def disp(tasks, my_todo_list):
    """
    Полный вывод
    """
    print("Еженедельные задачи~\n")
    display_list(my_todo_list)
    print("\n--------------~----------------\n")
    print("Список перпеменных задач~\n")
    display_list(tasks)
    print("\n")


def help_me():
    """
    Справка
    """
    print('? - Справка')
    print('ex - Сохранение и выход')
    print('add - Добавить запись')
    print('list - Просмотр записей')
    print('del - Удалить')
    print('cl - Очистить')
    print('upd - Обновить')


def main():
    # Создание списков задач
    tasks = []
    my_todo_list = {"пн": [],
                    "вт": [],
                    "ср": [],
                    "чт": [],
                    "пт": [],
                    "сб": [],
                    "вс": []
                    }
    # Запись сохраненной информации
    tasks, my_todo_list = upd(tasks, my_todo_list)
    # Вывод списков и справки
    disp(tasks, my_todo_list)
    help_me()
    # Бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'ex':
            save(tasks, my_todo_list)
            break

        elif command == 'add':
            cls()
            print("Создание новой записи~")
            choice = input("Вы хотите создать еженедельную задачу(1) "
                           "или на 1 день (2)? ")
            if choice == "1":
                new_week(my_todo_list)
            elif choice == "2":
                task = new_task()
                tasks.append(task)
                # Сортировка
                if len(tasks) > 1:
                    tasks.sort(key=lambda item: item.get('date', 0))
            save(tasks, my_todo_list)

        elif command == 'list':
            cls()
            disp(tasks, my_todo_list)

        elif command == 'del':
            print("Удаление записи-")
            choice = input("Вы хотите удалить еженедельную задачу(1),"
                           " на 1 день (2) или все(3)? ")
            if choice == "1":
                del_week(my_todo_list)
            elif choice == "2":
                del_task(tasks)
            elif choice == "3":
                choice = input("Вы хотите удалить все еженедельные задачи(1),"
                               "все однодневные задачи(2) или прям все(3)?")
                if choice == "1":
                    my_todo_list = {"пн": [],
                                    "вт": [],
                                    "ср": [],
                                    "чт": [],
                                    "пт": [],
                                    "сб": [],
                                    "вс": []
                                    }
                elif choice == "2":
                    tasks = []
                elif choice == "3":
                    my_todo_list = {"пн": [],
                                    "вт": [],
                                    "ср": [],
                                    "чт": [],
                                    "пт": [],
                                    "сб": [],
                                    "вс": []
                                    }
                    tasks = []
            save(tasks, my_todo_list)

        elif command == 'cl':
            cls()

        elif command == 'upd':
            upd(tasks, my_todo_list)

        elif command == '?':
            cls()
            help_me()
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
