from fastapi import FastAPI
from database.connection import init_db
from src.routers import auth_router

app = FastAPI(
    title="Weaver Studio API Backend",
    description= "API de gerenciamento de autenticação e controle de usuários VIP usando FastAPI e SQLite.",
    version="1.0.0"
)

init_db()

app.include_router(auth_router)

@app.get("/", tags=["Home"])

def home():
    return {
        "status": "online",
        "project": "Weaver Studio Backend",
        "architecture": "Clean Architecture "
    }