def classify_lead(message: str) -> str:
    message = message.lower()

    if "цена" in message or "стоимость" in message:
        return "sales"

    if "доставка" in message:
        return "logistics"

    if "ошибка" in message or "проблема" in message:
        return "support"

    return "other"
