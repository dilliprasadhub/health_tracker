# src/routes/save.py  (minimal example)
import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from twilio.rest import Client

from config import db
from utils import get_loggedin_user

router = APIRouter()

# load from env (use python-dotenv in development)
TW_SID = os.environ.get("US115b506c6ba8cef2bc8b991b19f9c028")
TW_TOKEN = os.environ.get("994564269aa047f2b0f16f3c3effabcb")
TW_FROM = os.environ.get("+917093756094")  # e.g. 'whatsapp:+1415...'

tw_client = Client(TW_SID, TW_TOKEN)

@router.post("/save-details")
def save_details(request: Request,
                 value: str = Form(...),     # example form fields
                 date: str = Form(...)):
    user = get_loggedin_user(request)
    if not user:
        return RedirectResponse("/login")

    # Build payload for Supabase
    payload = {
        "user_id": user.id,
        "value": value,
        "Date": str(date)   # convert to string 'YYYY-MM-DD' if needed
    }

    # INSERT into Supabase
    res = db.table("health_tracker").insert(payload).execute()

    # check success (supabase-py returns .data)
    if res.data:
        # prepare WhatsApp recipient — must be E.164 with whatsapp: prefix
        # Prefer reading phone from user record or DB. Here I assume user.phone exists.
        recipient = user.phone  # expect '+9198xxxx...' format
        if recipient:
            to_whatsapp = f"whatsapp:{recipient}"
        else:
            # fallback dev number (replace with real number)
            to_whatsapp = "whatsapp:+917093756094"

        # message body — keep it short & clear
        body = f"Hi {getattr(user,'name', '') or 'User'}, your entry on {payload['Date']} was saved. Value: {value}"

        # send message (wrapped in try/except so db insert is not lost)
        try:
            msg = tw_client.messages.create(
                from_=TW_FROM,
                to=to_whatsapp,
                body=body
            )
            # optional: log msg.sid
            print("Twilio SID:", msg.sid)
        except Exception as e:
            # log error — do NOT crash user flow because SMS failed
            print("Failed to send WhatsApp:", e)

    # return to dashboard (or render template)
    return RedirectResponse("/dashboard?date=" + str(payload["Date"]))
