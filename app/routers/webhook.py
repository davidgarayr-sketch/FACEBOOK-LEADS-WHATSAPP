import os
import hmac
import hashlib
from fastapi import APIRouter, Request, Query, HTTPException
from app.config import WEBHOOK_VERIFY_TOKEN, LEADS_APP_SECRET
from app.services.whatsapp import send_whatsapp_message
from app.routers.flows import flows

router = APIRouter()

def verify_signature(payload: bytes, signature: str) -> bool:
    if os.getenv("SKIP_SIGNATURE_CHECK") == "true":
        return True
    if not signature:
        return False
    expected = "sha256=" + hmac.new(
        key=LEADS_APP_SECRET.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

# Verificación del webhook (Facebook lo llama una sola vez para confirmar que el servidor existe)
@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    if hub_mode == "subscribe" and hub_token == WEBHOOK_VERIFY_TOKEN:
        return int(hub_challenge)
    return {"error": "Token inválido"}

# Recibir leads nuevos (Facebook llama esto cada vez que alguien llena un formulario)
@router.post("/webhook")
async def receive_lead(request: Request):

    # Verificar firma de Meta
    signature = request.headers.get("X-Hub-Signature-256", "")
    payload = await request.body()
    
    if not verify_signature(payload, signature):
        print("⚠️ Firma inválida — ignorando webhook")
        raise HTTPException(status_code=403, detail="Firma inválida")

    data = await request.json()
    print("📩 Lead recibido:", data)

    try:
        # Extrae información del Lead
        entry = data["entry"][0]
        changes = entry["changes"][0]
        lead_value = changes["value"]
        page_id = str(lead_value.get("page_id", ""))
        field_data = lead_value.get("field_data", [])

        # Obtiene el número de teléfono del Lead
        phone_number = None
        name = "Cliente"

        for field in field_data:
            if field["name"] == "phone_number":
                phone_number = field["values"][0]
            if field["name"] == "full_name":
                name = field["values"][0]

        # Buscar el flujo configurado para esta página
        flow = next((f for f in flows if f["page_id"] == page_id), None)

        if flow and phone_number:
            message = flow["message"].replace("{nombre}", name)
            send_whatsapp_message(phone_number, message)
            print(f"✅ Mensaje enviado a {phone_number}: {message}")
        elif phone_number:
            # Si no hay flujo configurado, usar mensaje por defecto
            send_whatsapp_message(phone_number, f"¡Hola {name}! Gracias por tu interés.")
            print(f"✅ Mensaje por defecto enviado a {phone_number}")
        else:
            print("⚠️ No se encontró número de teléfono")

    except Exception as e:
        print(f"❌ Error: {e}")

    return {"status": "ok"}