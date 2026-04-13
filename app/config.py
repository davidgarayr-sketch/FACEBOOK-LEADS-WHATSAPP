import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# App 1 - FLead_WSPIntegration
# Facebook Login
FB_APP_ID=os.getenv("FB_APP_ID")
FB_APP_SECRET=os.getenv("FB_APP_SECRET")

# App 2 - BGFLead_WSPIntegration
# Facebook Leads Ads + WhatsApp
LEADS_APP_ID = os.getenv("LEADS_APP_ID")
LEADS_APP_SECRET = os.getenv("LEADS_APP_SECRET")

# Webhook
WEBHOOK_VERIFY_TOKEN=os.getenv("WEBHOOK_VERIFY_TOKEN")

# WhatsApp
WHATSAPP_TOKEN=os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID=os.getenv("WHATSAPP_PHONE_ID")