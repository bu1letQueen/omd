# Guido van Rossum <guido@python.org>

def step1():
    print(
        "Утка-маляр 🦆 решила выпить зайти в бар. "
        "Взять ей зонтик? ☂️"
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()

def step2_umbrella():
    print("🦆 Утка взяла зонт и идёт по городу.")
    city = {
        "дом": ["парк"],
        "парк": ["мост", "дом"],
        "мост": ["площадь", "бар"],
        "площадь": ["бар", "парк"]
    }
    steps = 0
    position = "дом"

    while position != "бар":
        print(f"Сейчас утка в: {position}. Куда отправимся: {city[position]}?")
        choice = input("Куда идём? ")
        if choice in city[position]:
            position = choice
            steps += 1
        else:
            print("Выбери доступный маршрут, ботик")

        if steps > 3:
            print("АХТУНГ!! Начался дождь! Чтобы открыть зонт, нужно ввести код от него: (факториал 20)")
            code = input("Введите число: ")
            try:
                if int(code) == factorial(20):
                    print("Победа!️ Утки сегодня пьют")
                    return step3_bar()
                else:
                    print("Код неверный... Уточка промокла и заболела. Больным в бар путь закрыт")
                    return
            except:
                print("Это даже не число. Ты уже в баре? Квест для странников, пройди его в следующую пятницу")
                return
    print("Уточка добралась до бара в сухости и сохранности")
    return step3_bar()


def step2_no_umbrella():
    print("Утка без зонта идёт по длинному пути")
    city = {
        "дом": ["парк"],
        "парк": ["мост", "дом"],
        "мост": ["площадь", "бар"],
        "площадь": ["бар", "парк"]
    }
    steps = 0
    position = "дом"

    while position != "бар":
        print(f"Сейчас утка в: {position}. Доступные пути: {city[position]}")
        choice = input("Куда идём? ")
        if choice in city[position]:
            position = choice
            steps += 1
        else:
            print("Выбери доступный маршрут, ботик")

        if steps > 3:
            print("АХТУНГ!! Начался дождь! Уточке надо спуститься в канализацию, чтобы укрыться")
            return sewer_challenge()

    print("Уточка добралась до бара без зонта (и вся мокрая).")
    return step3_bar()


def sewer_challenge():
    print("Канализация. Нужно спуститься на 10 метров.")
    depth = 0
    while depth < 10:
        try:
            step = int(input("На сколько метров спускаемся? "))
            depth += step
            if depth < 10:
                print("Мало! Спускайся ещё")
            elif depth == 10:
                print("Уточка спустилась как Ювелир и встретила черепашек-ниндзя, ее прозвали Александром")
                print("Они налили ей глинтвейн и приняли в команду. Победа! ")
                return
            else:
                print("Уточка захлебнулась. Миссия провалена")
                return
        except:
            print("Это даже не число. Ты уже в баре? Квест для странников, пройди его в следующую пятницу")
    return


def step3_bar():
    print("Бармен спрашивает: 'Что будете пить? Водка или пиво?'")
    option = ''
    options = {'водка': "vodka", 'пиво': "beer"}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if option == 'водка':
        print("На утро уточка очнулась в канаве. Миссия провалена ")
    else:
        print("Уточка выбрала пиво. Вечер был хорош, победа")


def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == '__main__':
    step1()
