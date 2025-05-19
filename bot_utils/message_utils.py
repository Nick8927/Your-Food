def text_for_caption(name, description, price) -> str:
    """формирует текст для описания продукта в сообщении под изображением"""
    return (
        f"<b>{name}</b>\n\n"
        f"<b>Описание:</b>{description}\n\n"
        f"<b>Цена:</b> {price:.2f} BYN"
    )
