from logger import logger

def log_user_registration(user_id: int, username: str):
    """лог регистрацию юзера"""
    logger.info(f"[USER_ACTION] User {user_id} (username: @{username}) registered")

def log_user_order(user_id: int, order_id: int, total_price: float):
    """лог заказ юзера"""
    logger.info(f"[USER_ACTION] User {user_id} placed order #{order_id} for {total_price:.2f} BYN")

def log_user_deletion(user_id: int):
    """лог удаление аккаунта юзера"""
    logger.info(f"[USER_ACTION] User {user_id} deleted account")
