import os
from pathlib import Path

PROMPT_PATH = Path(__file__).parent / "classifier_prompt.md"


def load_classifier_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def classify_with_ai(message: str) -> str:
    provider = os.getenv("AI_PROVIDER", "mock")

    if provider == "mock":
        return classify_mock(message)

    raise RuntimeError(f"Unsupported AI_PROVIDER: {provider}")


def classify_mock(message: str) -> str:
    message = message.lower()

    support_words = [
        "ошиб",
        "проблем",
        "не работает",
        "слом",
    ]

    sales_words = [
        "цен",
        "стоим",
        "заказ",
        "куп",
        "расчёт",
        "расчет",
        "изготовлен",
    ]

    logistics_words = [
        "достав",
        "отправ",
        "транспорт",
        "перевоз",
    ]

    if any(word in message for word in support_words):
        return "support"

    if any(word in message for word in sales_words):
        return "sales"

    if any(word in message for word in logistics_words):
        return "logistics"

    return "other"