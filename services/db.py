from sqlalchemy import create_engine, text
import os

DB_URL = os.getenv("DB_URL", "sqlite:///cashierless.db")
engine = create_engine(DB_URL, echo=False)

def init_db():
    with engine.begin() as conn:
        with open("services/schema.sql") as f:
            conn.execute(text(f.read()))
