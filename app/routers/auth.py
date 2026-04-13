from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import httpx
from app.config import FB_APP_ID, FB_APP_SECRET

router = APIRouter()

REDIRECT_URI = "https://facebook-leads-whatsapp-production.up.railway.app/auth/callback"

@router.get("/auth/login")
async def facebook_login():
    #Redirige al usuario a Facebook para autorizar la app.
    fb_auth_url = (
        f"https://www.facebook.com/v21.0/dialog/oauth"
        f"?client_id={FB_APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=public_profile"
    )
    return RedirectResponse(url=fb_auth_url)

@router.get("/auth/callback")
async def facebook_callback(code: str = None, error: str = None):
    #Facebook redirige aquí después de que el usuario autoriza.
    
    if error:
        return {"error": f"El usuario canceló o hubo un error: {error}"}
    
    if not code:
        return {"error": "No se recibió código de autorización"}

    # Intercambiar el código por un access token
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://graph.facebook.com/v21.0/oauth/access_token",
            params={
                "client_id": FB_APP_ID,
                "client_secret": FB_APP_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code
            }
        )
    
    token_data = response.json()
    
    if "access_token" in token_data:
        access_token = token_data["access_token"]
        print(f"✅ Token obtenido: {access_token[:20]}...")
        # Redirigir al Flow Builder con éxito
        return RedirectResponse(url="/?connected=true", status_code=302)
    else:
        return {"error": "No se pudo obtener el token", "details": token_data}