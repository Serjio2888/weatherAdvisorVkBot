import api
import db
import vk_api_worker
import utils
from constants import answers


# for WeatherAdvisor
def weather(message, uid):
    query = message.split(" ", 1)
    if len(query) < 2:
        result, ok = db.get_user_info(uid)
        if not ok:
            return {"answer": "",
                    "status": 10}
        else:
            city = result[2]
    else:
        city = query[1]
    answer, ok, _ = api.weather(city)
    if ok:
        return {"answer": answer,
                "status": 200}
    else:
        return {"answer": "",
                "status": 11}


def town(message, uid):
    query = message.split(" ", 1)
    if len(query) < 2:
        return {"answer": "",
                "status": 20}
    _, ok = db.get_user_info(uid)
    if ok:
        ok2 = db.update_town(uid, query[1])
    else:
        name, surname = vk_api_worker.get_user_names(uid)
        ok2 = db.add_user(uid, query[1], name, surname)
    if not ok2:
        return {"answer": "",
                "status": 100}
    if ok:
        return {"answer": answers[2],
                "status": 200}
    else:
        return {"answer": answers[1],
                "status": 200}


def add_notification(message, uid):
    query = message.split(" ", 1)
    if len(query) < 2:
        return {"answer": "",
                "status": 41}
    _, ok = db.get_user_info(uid)
    if not ok:
        return {"answer": "",
                "status": 43}
    hour = query[1]
    try:
        hour = int(hour)
    except ValueError:
        return {"answer": "",
                "status": 41}
    if hour < 0 or hour > 23:
        return {"answer": "",
                "status": 42}
    db.update_timer(hour, uid)
    return {"answer": answers[40],
            "status": 200}


def advise(message, uid):
    result, ok = db.get_user_info(uid)
    if not ok:
        return {"answer": "",
                "status": 30}
    city = result[2]
    _, ok, pogoda = api.weather(city)
    if not ok:
        return {"answer": "",
                "status": 11}
    return {"answer": utils.do_pogoda_advise(pogoda),
            "status": 200}


def default():
    return {"answer": answers[20],
            "status": 200}


def begin():
    return {"answer": answers[30],
            "status": 200}


# for Cron
def notify(now):
    users, ok = db.get_users_by_time(now)
    if ok:
        notifications = []
        for user in users:
            info, ok, pogoda = api.weather(user["city"])
            if not ok:
                notifications.append({"answer": "",
                                      "uid": user["uid"],
                                      "status": 40})
            else:
                notifications.append({"answer": utils.collect_notification(info, pogoda, user["name"]),
                                      "uid": user["uid"],
                                      "status": 200})
        return notifications
    return []
