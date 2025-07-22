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


def log_user_order(username: str, user_id: int, orders_data: list, total_price: float):
    """лог заказа юзера с деталями товаров и добавок"""
    log_text = f"[USER_ACTION] Пользователь {username} (ID: {user_id}) оформил заказ:\n"
    for order in orders_data:
        log_text += f"- {order['name']} ({order['quantity']} шт.) — {order['price']:.2f} BYN\n"
        if order["addons"]:
            addons_str = ", ".join([f"{a['name']} ({a['price']:.2f})" for a in order["addons"]])
            log_text += f"  Добавки: {addons_str}\n"
        else:
            log_text += f"  Добавки: Нет\n"
    log_text += f"Общая сумма: {total_price:.2f} BYN"
    logger.info(log_text)


