from fastapi import FastAPI
from app.routers import webhook, flows, auth

# Aplicación principal
app = FastAPI(title="Facebook Leads + WhatsApp Integration")

# Registra las rutas
app.include_router(flows.router)
app.include_router(webhook.router, prefix="/api")
app.include_router(auth.router)