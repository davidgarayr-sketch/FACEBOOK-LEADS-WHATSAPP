import json
import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

FLOWS_FILE = "flows.json"

def load_flows():
    if os.path.exists(FLOWS_FILE):
        with open(FLOWS_FILE, "r") as f:
            return json.load(f)
    return []

def save_flows(flows):
    with open(FLOWS_FILE, "w") as f:
        json.dump(flows, f, indent=2)

flows = load_flows()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, connected: str = None):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"success": False, "connected": connected is not None}
    )

@router.post("/save-flow", response_class=HTMLResponse)
async def save_flow(
    request: Request,
    page_id: str = Form(...),
    form_id: str = Form(...),
    message: str = Form(...),
    phone_id: str = Form(...)
):
    flow = {
        "page_id": page_id,
        "form_id": form_id,
        "message": message,
        "phone_id": phone_id
    }
    flows.append(flow)
    save_flows(flows)
    print(f"Flujo guardado: {flow}")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"success": True}
    )