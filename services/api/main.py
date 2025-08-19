from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text
from services.db import engine, init_db
from datetime import datetime
import random

app = FastAPI()
init_db()

class EnterReq(BaseModel):
    user_token: str | None = None

@app.post("/enter")
def enter(req: EnterReq):
    person_id = f"user_{random.randint(1000,9999)}"
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO person_session (person_id, entry_time) VALUES (:pid, :t)"),
                     {"pid": person_id, "t": datetime.utcnow()})
    return {"person_id": person_id}

@app.post("/exit/{person_id}")
def exit_store(person_id: str):
    with engine.begin() as conn:
        cart = conn.execute(text("SELECT sku, qty, unit_price FROM cart_line WHERE person_id=:pid"),
                            {"pid": person_id}).fetchall()
        total = sum([c.qty * c.unit_price for c in cart])
        pay_ref = f"upi_txn_{random.randint(1000,9999)}"
        conn.execute(text("INSERT INTO receipt (person_id, total, ts, pay_ref, status) VALUES (:p,:t,:ts,:r,:s)"),
                     {"p": person_id, "t": total, "ts": datetime.utcnow(), "r": pay_ref, "s": "paid"})
        conn.execute(text("UPDATE person_session SET exit_time=:t WHERE person_id=:p"),
                     {"p": person_id, "t": datetime.utcnow()})
    return {"person_id": person_id, "items": [dict(c) for c in cart], "total": total, "pay_ref": pay_ref}
