# AI Lead Router

A lightweight AI-powered lead routing service built with FastAPI, Ollama and SQLite.

The project demonstrates a simple business automation pipeline:

**Incoming lead → AI classification → Database → CRM adapter → Status update**

## What it does

The service accepts customer leads through a REST API and automatically classifies the customer's primary intent into one of four categories:

- `sales` — purchase, pricing, quotation or product inquiries
- `logistics` — delivery, shipment or transportation inquiries
- `support` — problems with an existing product, order or service
- `other` — unrelated or unclear requests

After classification, the lead is stored in SQLite and passed to a CRM adapter.

## Architecture

```text
                    ┌─────────────────┐
                    │   Incoming Lead │
                    │    REST / API   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │   /leads POST   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Ollama / Llama │
                    │      3.2:3b     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Classification │
                    │ sales / logistics│
                    │ support / other │
                    └────────┬────────┘
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
          ┌─────────────────┐  ┌─────────────────┐
          │     SQLite      │  │   CRM Adapter   │
          │   Lead storage  │  │    Bitrix24*    │
          └────────┬────────┘  └────────┬────────┘
                   └─────────┬──────────┘
                             ▼
                       Status update
````

* The current CRM integration is implemented as a mock adapter. It represents the integration boundary where a real Bitrix24 API can be connected.

## Tech stack

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* Ollama
* Llama 3.2 3B
* REST API
* Git / GitHub

## Project structure

```text
01-ai-lead-router/
│
├── ai/
│   ├── classifier.py
│   └── classifier_prompt.md
│
├── main.py
├── database.py
├── crm.py
├── requirements.txt
├── .gitignore
└── README.md
```

## API

### `GET /`

Health check.

Example response:

```json
{
  "message": "AI Lead Router is running"
}
```

### `GET /prompt`

Returns the current classification prompt.

### `GET /leads`

Returns leads stored in the database.

### `POST /leads`

Accepts a new lead.

Example request:

```json
{
  "name": "Ivan",
  "email": "ivan@example.com",
  "message": "How much will delivery to Rostov cost?"
}
```

Example response:

```json
{
  "status": "received",
  "id": 5,
  "category": "logistics",
  "db_status": "sent_to_crm",
  "crm": {
    "crm": "bitrix24",
    "lead_id": 5,
    "status": "created",
    "category": "logistics"
  }
}
```

## AI classification

The classifier uses a dedicated prompt stored in:

```text
ai/classifier_prompt.md
```

The prompt defines:

* available categories;
* classification rules;
* priority rules for conflicting intents;
* examples;
* strict output requirements.

The application uses Ollama locally, so no external LLM API key is required.

The AI provider is configurable through the `AI_PROVIDER` environment variable.

```text
AI_PROVIDER=ollama
```

A mock classifier is also retained for development and testing:

```text
AI_PROVIDER=mock
```

## Error handling

CRM communication is isolated from lead persistence.

If the CRM adapter fails, the lead remains stored in the database and receives the status:

```text
crm_error
```

This prevents a CRM failure from losing an already received lead.

## Running locally

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running and the model is available:

```bash
ollama list
```

The project currently uses:

```text
llama3.2:3b
```

Set the AI provider:

```powershell
$env:AI_PROVIDER="ollama"
```

Start the API:

```bash
uvicorn main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Example workflow

A customer submits:

```text
How much will delivery to Rostov cost?
```

The application:

1. receives the lead through FastAPI;
2. sends the message to the local Llama model;
3. classifies the intent as `logistics`;
4. stores the lead in SQLite;
5. sends it to the CRM adapter;
6. updates the lead status to `sent_to_crm`.

## Development approach

The project was built using AI-assisted development with an emphasis on:

* decomposition of business requirements into small components;
* prompt design and iteration;
* API and database integration;
* explicit error handling;
* separation of AI, persistence and CRM layers;
* testing AI behaviour with representative inputs.

The architecture is intentionally simple and designed to be extended with real CRM APIs, webhooks, authentication, background jobs and additional AI providers.
