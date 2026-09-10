from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ai.classifier import classify_with_ai, load_classifier_prompt
from database import LeadDB, SessionLocal
from crm import send_to_crm


app = FastAPI()


class Lead(BaseModel):
    name: str
    email: str
    message: str


@app.get("/")
def root():
    return {"message": "AI Lead Router is running"}


@app.get("/prompt")
def get_prompt():
    return {"prompt": load_classifier_prompt()}


@app.get("/leads")
def get_leads():
    db: Session = SessionLocal()

    leads = db.query(LeadDB).all()

    result = [
        {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "message": lead.message,
            "category": lead.category,
            "status": lead.status,
        }
        for lead in leads
    ]

    db.close()

    return {"leads": result}

@app.post("/leads")
def create_lead(lead: Lead):
    category = classify_with_ai(lead.message)

    db: Session = SessionLocal()

    new_lead = LeadDB(
        name=lead.name,
        email=lead.email,
        message=lead.message,
        category=category,
        status="new",
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    crm_result = send_to_crm(
        lead_id=new_lead.id,
        name=lead.name,
        email=lead.email,
        message=lead.message,
        category=category,
    )

    new_lead.status = "sent_to_crm"
    db.commit()

    lead_id = new_lead.id
    db_status = new_lead.status

    db.close()

    return {
        "status": "received",
        "id": lead_id,
        "category": category,
        "db_status": db_status,
        "crm": crm_result,
        "lead": lead,
    }