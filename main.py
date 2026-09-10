from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Lead(BaseModel):
    name: str
    email: str
    message: str


@app.get("/")
def root():
    return {"message": "AI Lead Router is running"}


def classify_lead(message: str) -> str:
    message = message.lower()

    sales_words = ["цен", "стоим", "заказ", "куп"]
    logistics_words = ["достав", "отправ"]
    support_words = ["ошиб", "проблем", "не работает"]

    if any(word in message for word in sales_words):
        return "sales"

    if any(word in message for word in logistics_words):
        return "logistics"

    if any(word in message for word in support_words):
        return "support"

    return "other"


@app.post("/leads")
def create_lead(lead: Lead):
    category = classify_lead(lead.message)

    return {
        "status": "received",
        "category": category,
        "lead": lead
    }
