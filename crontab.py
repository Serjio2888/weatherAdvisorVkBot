from random import randint
from time import sleep
from datetime import datetime
import pytz

import delivery
import settings
from constants import statuses as status


class Cron:
    def __init__(self, log):
        self.log = log
        self.longpoll, self.vk, self.keyboard = settings.vk_init()

    def send(self, message, uid):
        self.vk.messages.send(
            user_id=uid,
            message=message,
            keyboard=self.keyboard.get_keyboard(),
            random_id=randint(0, 10000000),
        )

    @staticmethod
    def count_time():
        time = datetime.now(pytz.timezone("Europe/Moscow"))  # так как сервер в Лондоне
        seconds_left = (60 - time.minute) * 60
        return time.hour, seconds_left

    def proceed(self):
        now, seconds_left = self.count_time()
        answers = delivery.notify(now)
        if len(answers):
            bad = 0
            for answer in answers:
                if answer["status"] == 200:
                    self.send(answer["answer"], answer["uid"])
                    bad += 1
                else:
                    self.send(status[answer["status"]], answer["uid"])
            self.log.info("Время - {} часов. Уведомлений отправлено {}. Из них с проблемами - {}".
                          format(now, len(answers), bad))
        else:
            self.log.info("Время - {} часов. Уведомлений отправлено не было.".format(now))
        return seconds_left

    def run(self):
        while True:
            seconds_left_until_next_hour = self.proceed()
            sleep(seconds_left_until_next_hour)
