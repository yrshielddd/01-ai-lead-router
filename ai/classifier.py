import os
from pathlib import Path

import requests


PROMPT_PATH = Path(__file__).parent / "classifier_prompt.md"

ALLOWED_CATEGORIES = {
    "sales",
    "logistics",
    "support",
    "other",
}


def load_classifier_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def classify_with_ai(message: str) -> str:
    provider = os.getenv("AI_PROVIDER", "ollama")

    if provider == "mock":
        return classify_mock(message)

    if provider == "ollama":
        return classify_ollama(message)

    raise RuntimeError(f"Unsupported AI_PROVIDER: {provider}")


def classify_ollama(message: str) -> str:
    prompt = load_classifier_prompt()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": f"{prompt}\n\nCustomer message:\n{message}",
            "stream": False,
        },
        timeout=60,
    )

    response.raise_for_status()

    result = response.json()["response"].strip().lower()

    for category in ALLOWED_CATEGORIES:
        if category in result:
            return category

    return "other"


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