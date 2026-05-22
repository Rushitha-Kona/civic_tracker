from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import uuid
import joblib
import requests
import re

from db import collection

app = FastAPI()

# -------------------------------
# Frontend
# -------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")


# -------------------------------
# Load ML Model
# -------------------------------
model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


# -------------------------------
# Sessions (WhatsApp flow tracking)
# -------------------------------
user_sessions = {}


# -------------------------------
# Request Schema (API use)
# -------------------------------
class Complaint(BaseModel):
    text: str
    location: str = "Unknown"
    image_url: str = None


# -------------------------------
# ML Classification
# -------------------------------
def classify_issue(text):
    text_vec = vectorizer.transform([text])
    return model.predict(text_vec)[0]


# -------------------------------
# Reverse Geocoding
# -------------------------------
def get_location_name(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        res = requests.get(url, headers={"User-Agent": "civic-app"})
        return res.json().get("display_name", "Unknown")
    except:
        return "Unknown"


# -------------------------------
# Extract location from WhatsApp text
# -------------------------------
def extract_location(text):
    patterns = [
        r"q=([0-9\.\-]+),([0-9\.\-]+)",
        r"@([0-9\.\-]+),([0-9\.\-]+)"
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            return match.group(1), match.group(2)

    return None, None


# -------------------------------
# API: Manual report
# -------------------------------
@app.post("/report")
def report_issue(complaint: Complaint):

    category = classify_issue(complaint.text)
    complaint_id = "C" + str(uuid.uuid4())[:5]

    data = {
        "complaint_id": complaint_id,
        "text": complaint.text,
        "category": category,
        "location": complaint.location,
        "image_url": complaint.image_url,
        "status": "Pending",
        "created_at": datetime.now()
    }

    collection.insert_one(data)

    return {
        "message": "Complaint registered",
        "complaint_id": complaint_id,
        "category": category
    }


# -------------------------------
# API: Get all complaints
# -------------------------------
@app.get("/all")
def get_all():
    return list(collection.find({}, {"_id": 0}))


# -------------------------------
# API: Update status
# -------------------------------
@app.put("/update/{complaint_id}")
def update_status(complaint_id: str, status: str):

    result = collection.update_one(
        {"complaint_id": complaint_id},
        {"$set": {"status": status}}
    )

    return {"message": "Updated" if result.modified_count else "Not found"}


# -------------------------------
# WhatsApp Webhook (FULL FLOW)
# -------------------------------
def normalize_user(user):
    return user.replace("whatsapp:", "").strip() if user else "unknown"


@app.post("/whatsapp")
async def whatsapp(request: Request):

    form = await request.form()

    text = form.get("Body") or ""
    user = normalize_user(form.get("From"))
    image_url = form.get("MediaUrl0")

    lat, lon = extract_location(text)

    # -------------------------
    # STEP 1: TEXT RECEIVED
    # -------------------------
    if text and not image_url and not lat:
        user_sessions[user] = {
            "text": text,
            "image": None
        }

        reply = "📸 Send photo OR send location link"

        return PlainTextResponse(
            f"<Response><Message>{reply}</Message></Response>",
            media_type="application/xml"
        )

    # -------------------------
    # STEP 2: IMAGE RECEIVED
    # -------------------------
    if image_url:
        if user not in user_sessions:
            user_sessions[user] = {}

        user_sessions[user]["image"] = image_url

        reply = "📍 Now send your location link"

        return PlainTextResponse(
            f"<Response><Message>{reply}</Message></Response>",
            media_type="application/xml"
        )

    # -------------------------
    # STEP 3: LOCATION RECEIVED
    # -------------------------
    if lat and lon:

        if user not in user_sessions:
            return PlainTextResponse(
                "<Response><Message>Send complaint first</Message></Response>",
                media_type="application/xml"
            )

        complaint_text = user_sessions[user].get("text", text)
        image_url = user_sessions[user].get("image")

        location = get_location_name(lat, lon)
        category = classify_issue(complaint_text)

        complaint_id = "C" + str(uuid.uuid4())[:5]

        data = {
            "complaint_id": complaint_id,
            "text": complaint_text,
            "category": category,
            "location": location,
            "image_url": image_url,
            "status": "Pending",
            "created_at": datetime.now()
        }

        collection.insert_one(data)

        del user_sessions[user]

        reply = f"✅ Registered!\nID: {complaint_id}\nCategory: {category}"

        return PlainTextResponse(
            f"<Response><Message>{reply}</Message></Response>",
            media_type="application/xml"
        )

    return PlainTextResponse(
        "<Response><Message>Send complaint text</Message></Response>",
        media_type="application/xml"
    )