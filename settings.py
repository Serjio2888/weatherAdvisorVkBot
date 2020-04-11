import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import logging
from credentials import vk_token


def logger_init():
    logging.basicConfig(filename="wadvisor.log",
                        format='%(asctime)s:%(name)s:%(levelname)s: %(message)s',
                        level=logging.INFO)
    return logging


def vk_init():
    token = vk_token
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    keyboard1 = VkKeyboard(one_time=True)
    keyboard1.add_button('Погода', color=VkKeyboardColor.PRIMARY)
    keyboard1.add_button('Совет', color=VkKeyboardColor.PRIMARY)
    return longpoll, vk, keyboard1
