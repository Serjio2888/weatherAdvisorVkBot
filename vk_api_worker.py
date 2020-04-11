from settings import vk_init

_, _vk, _ = vk_init()


def get_user_names(uid):
    info = _vk.users.get(user_ids=uid)[0]
    return info["first_name"], info["last_name"]

