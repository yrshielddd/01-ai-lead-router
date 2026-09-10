def send_to_crm(lead_id: int, name: str, email: str, message: str, category: str):
    return {
        "crm": "bitrix24",
        "lead_id": lead_id,
        "status": "created",
        "category": category,
    }