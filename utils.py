from random import choice

from constants import answers, greetings, endings
import db


def do_pogoda_advise(pogoda):
    describe = pogoda[0]
    wind = pogoda[1]
    if wind > 12:  # ветер - первостепенно
        return choice(answers[15])
    if 'ясно' in describe:
        return choice(answers[10])
    if 'дождь' in describe:
        return choice(answers[11])
    if 'пасмурно' in describe:
        return choice(answers[12])
    if 'облачно' in describe:
        return choice(answers[13])
    return choice(answers[14])


def do_film_advise(pogoda):
    describe = pogoda[0]
    wind = pogoda[1]
    if wind > 12:  # ветер - первостепенно
        return db.get_film_by_weather("windy")
    if 'ясно' in describe:
        return db.get_film_by_weather("fair")
    if 'дождь' in describe:
        return db.get_film_by_weather("rainy")
    if 'пасмурно' in describe:
        return db.get_film_by_weather("cloudy")
    if 'облачно' in describe:
        return db.get_film_by_weather("cloudy")
    return db.get_film_by_weather("rainy")


def collect_notification(info, pogoda, name):
    message = ""
    message += choice(greetings) + ", " + name + "!\n\n"
    message += info + "\n"
    message += do_pogoda_advise(pogoda) + "\n\n"
    message += "Сегодня советую глянуть фильм " + do_film_advise(pogoda) + "\n\n"
    message += choice(endings)
    return message
