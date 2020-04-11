from random import randint
import multiprocessing
from vk_api.longpoll import VkEventType

import delivery
import settings
from constants import statuses as status
from crontab import Cron


class WeatherAdvisorMain:
    def __init__(self, log):
        self.log = log
        self.longpoll, self.vk, self.keyboard = settings.vk_init()

    def deliverer(self, uid, message):
        if message.startswith("погода"):
            answer = delivery.weather(message, uid)
        elif message.startswith("совет"):
            answer = delivery.advise(message, uid)
        elif message.startswith("город"):
            answer = delivery.town(message, uid)
        elif message.startswith("уведомление"):
            answer = delivery.add_notification(message, uid)
        elif message.startswith("/start") or 'старт' in message:
            answer = delivery.begin()
        else:
            answer = delivery.default()

        if answer["status"] == 200:
            self.log.info("УСПЕХ! Юзеру {} отправлено '{}'".format(uid, answer["answer"]))
            return self.send(answer["answer"], uid)
        else:
            self.log.info("ПРОБЛЕМА! Юзеру {} отправлено '{}'".format(uid, status[answer["status"]]))
            return self.send(status[answer["status"]], uid)

    def send(self, message, uid):
        self.vk.messages.send(
            user_id=uid,
            message=message,
            keyboard=self.keyboard.get_keyboard(),
            random_id=randint(0, 10000000),
        )

    def run(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                if event.from_user:
                    self.deliverer(event.user_id, event.message.lower())


if __name__ == "__main__":
    logging = settings.logger_init()
    cron = Cron(logging.getLogger("notify"))
    cron = multiprocessing.Process(target=cron.run, args=())
    cron.start()

    wa = WeatherAdvisorMain(logging.getLogger("main"))
    wa = multiprocessing.Process(target=wa.run, args=())
    wa.start()
