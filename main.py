from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.connect(dsn=os.getenv("SUPABASE_DB_URL"))

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/payers")
async def get_payers():
    rows = await app.state.db.fetch("SELECT * FROM payers")
    return [dict(r) for r in rows]

@app.get("/payments")
async def get_payments():
    rows = await app.state.db.fetch("SELECT * FROM payments")
    return [dict(r) for r in rows]

@app.get("/joined-payments")
async def get_joined_data():
    rows = await app.state.db.fetch("""
        SELECT p.full_name, p.country, p.email, pay.*
        FROM payments pay
        JOIN payers p ON pay.payer_id = p.payer_id
    """)
    return [dict(r) for r in rows]