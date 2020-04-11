from random import choice

from constants import answers, greetings, endings


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


def collect_notification(info, pogoda, name):
    message = ""
    message += choice(greetings) + ", " + name + "!\n\n"
    message += info + "\n"
    message += do_pogoda_advise(pogoda) + "\n\n"
    message += choice(endings)
    return message
