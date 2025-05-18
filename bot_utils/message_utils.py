def text_for_caption(name, description, price) -> str:
    return (
        f"<b>{name}</b>\n\n"
        f"{description}\n\n"
        f"<b>Цена:</b> {price:.2f} BYN"
    )
