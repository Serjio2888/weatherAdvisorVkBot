import requests
from datetime import datetime


def weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    parameters = {
        'q': city,
        'appid': "778d98cf94b6609bec655b872f24b907",
        'units': 'metric',
        'lang': 'ru'
    }
    res = requests.get(url, params=parameters)
    data = res.json()
    if data['cod'] == 200:
        sunset = datetime.fromtimestamp(data["sys"]["sunset"])
        sunset = str(sunset.hour+3)+":"+str(sunset.minute)
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunrise = str(sunrise.hour+3) + ":" + str(sunrise.minute)
        pogoda = data["weather"][0]["description"]
        msg = "Погода в городе " + city.capitalize() + ':\n\n'
        msg += pogoda + '\n'
        msg += "Температура: " + str(data["main"]["temp"]) + "℃" + '\n'
        msg += "Ощущается как " + str(data["main"]["feels_like"]) + "℃" + '\n'
        msg += "Скорость ветра: " + str(data["wind"]["speed"]) + " м/с" + '\n'
        msg += "Рассвет: " + sunrise + ". Закат: " + sunset + '\n'
        return msg, True, [pogoda, data["wind"]["speed"]]
    else:
        return "", False, None

