import csv

with open('Corp_Summary.csv', 'r',  newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    employees = list(reader)

def build_hierarchy(employees: list) -> dict:
    departments = {}
    for employee in employees:
        if employee['Департамент'] not in departments:
            departments[employee['Департамент']] = set()
        departments[employee['Департамент']].add(employee['Отдел'])

    for department in departments:
        print(f"{department}: {', '.join(departments[department])}")

    return


build_hierarchy(employees)





