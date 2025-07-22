from logger import logger


def log_user_registration(username: str, phone: str | None = None):
    """лог регистрации юзера"""
    if phone:
        logger.info(f"[USER_ACTION] Пользователь @{username} (тел.: {phone}) зарегистрировался")
    else:
        logger.info(f"[USER_ACTION] Пользователь @{username} начал регистрацию...")


def log_user_phone_update(username: str, phone: str):
    """лог добавления номера телефона"""
    logger.info(f"[USER_ACTION] Пользователь @{username} добавил номер тел.: {phone}")


