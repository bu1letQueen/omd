import csv


def read_file(filename: str) -> list[dict[str, str]]:
    """
    Читает csv-файл с сотрудниками

    :param filename: путь к файлу csv
    :return: список словарей с данными о сотрудниках
    """
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        return list(reader)


def build_hierarchy(employees: list[dict[str, str]]) -> dict[str, set[str]]:
    """
    Строит иерархию департаментов по командам

    :param employees: список сотрудников
    :return: словарь {департамент: множество команд}
    """
    departments: dict[str, set[str]] = {}
    for employee in employees:
        dep = employee['Департамент']
        team = employee['Отдел']
        if dep not in departments:
            departments[dep] = set()
        departments[dep].add(team)
    return departments


def make_report(employees: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    """
    Формирует сводный отчет по департаментам

    :param employees: список сотрудников
    :return: словарь {департамент: {count, sum, min, max, mean}}
    """
    acc: dict[str, dict[str, float]] = {}
    for employee in employees:
        dep = employee['Департамент']
        salary = int(employee['Оклад'])
        if dep not in acc:
            acc[dep] = {
                'count': 0,
                'sum': 0,
                'min': salary,
                'max': salary
            }
        acc[dep]['count'] += 1
        acc[dep]['sum'] += salary
        acc[dep]['min'] = min(salary, acc[dep]['min'])
        acc[dep]['max'] = max(salary, acc[dep]['max'])
    for dep in acc:
        acc[dep]['mean'] = round(acc[dep]['sum'] / acc[dep]['count'], 2)
    return acc


def pretty_output(title: str):
    """
    Декоратор: печатает заголовок и рамку вокруг функции вывода

    :param title: заголовок, который будет выведен
    """

    def decorator(func):
        def wrapper(data: dict):
            print("=" * 60)
            print(title.center(60))
            print("=" * 60)
            func(data)
            print("=" * 60)

        return wrapper

    return decorator


@pretty_output("СВОДНЫЙ ОТЧЁТ ПО ДЕПАРТАМЕНТАМ")
def print_report(report: dict[str, dict[str, float]]) -> None:
    """
    Печатает сводный отчет по департаментам с выравниванием

    :param report: словарь с данными из make_report
    """
    print(f"{'Департамент':20} {'Число':>6} {'МинЗП':>8} {'МаксЗП':>8} {'СредЗП':>10}")
    print("-" * 60)
    for dep, data in sorted(report.items()):
        print(f"{dep:20} {data['count']:6} {data['min']:8} {data['max']:8} {data['mean']:10}")


@pretty_output("ИЕРАРХИЯ КОМАНД ПО ДЕПАРТАМЕНТАМ")
def print_hierarchy(hierarchy: dict[str, set[str]]) -> None:
    """
    Печатает иерархию департаментов по командам с выравниванием

    :param hierarchy: словарь {департамент: множество команд}
    """
    for dep, teams in sorted(hierarchy.items()):
        print(dep.ljust(20), ":", ", ".join(sorted(teams)))


def save_report(report: dict[str, dict[str, float]], filename: str) -> None:
    """
    Сохраняет сводный отчёт в csv-файл

    :param report: словарь с данными из make_report
    :param filename: имя выходного CSV-файла
    """
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Департамент", "Численность", "МинЗП", "МаксЗП", "СредняяЗП"])
        for dep, data in sorted(report.items()):
            writer.writerow([dep, data["count"], data["min"], data["max"], data["mean"]])
    print('Файл успешно сохранён:', filename)


def show_menu() -> None:
    """
    Показывает доступные опции по обработке файла
    """
    print("\nВыберите одну из доступных опций:")
    print("1 -- Посмотреть иерархию команд")
    print("2 -- Получить сводный отчёт по департаментам")
    print("3 -- Сохранить сводный отчёт")
    print("0 -- Завершить работу")


def main_menu() -> None:
    """
    Главное меню программы, управляющее выбором пользователя
    """
    employees = read_file("Corp_Summary.csv")
    while True:
        show_menu()
        choose = int(input("Выберите команду: "))

        if choose == 1:
            print_hierarchy(build_hierarchy(employees))
        elif choose == 2:
            print_report(make_report(employees))
        elif choose == 3:
            filename = input("Введите имя файла для отчета: ")
            save_report(make_report(employees), filename)
        elif choose == 0:
            break
        else:
            print("Введите число 0/1/2/3")


if __name__ == "__main__":
    main_menu()
