**Civic Issue Tracker 🚨**
An AI-powered Civic Issue Tracking System built using FastAPI, MongoDB, Machine Learning, and WhatsApp integration using Twilio.
This project allows citizens to report public issues like:
Garbage problems
Water leakage
Road damage
Street light issues
Drainage complaints
**Users can submit complaints through:**
🌐 Web Dashboard
📱 WhatsApp Chatbot
The system automatically classifies complaints using a Machine Learning model and stores them in MongoDB.
**🚀 Features**
✅ AI Complaint Classification
Uses a trained ML model to classify complaints into categories.
Examples:
"Garbage near my house" → Garbage
"Street lights not working" → Electricity
✅ WhatsApp Complaint Registration
Users can send complaints through WhatsApp.
**Flow:**
Send complaint text
Send optional image
Send Google Maps location
Complaint gets registered automatically
✅ Location Detection
Extracts latitude & longitude from Google Maps links and converts them into real addresses using OpenStreetMap API.
✅ Admin Dashboard
**Dashboard shows:**
Complaint ID
Category
Status
Location
Complaint Image
Admin can:
View all complaints
Update complaint status
✅ MongoDB Storage
All complaints are stored permanently in MongoDB.
**🛠️ Technologies Used**
Python
FastAPI
MongoDB
Scikit-learn
Joblib
Twilio WhatsApp API
HTML
CSS
JavaScript
**📂 Project Structure**

civic-tracker/
│
├── app.py
├── db.py
├── requirements.txt
│
├── models/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
**⚙️ Installation**
1️⃣ Clone Project
Bash
git clone <your-repository-link>
cd civic-tracker
2️⃣ Create Virtual Environment
Bash
python -m venv .venv
Activate virtual environment:
Windows
Bash
.venv\Scripts\activate
3️⃣ Install Requirements
Bash
pip install -r requirements.txt
▶️ Run Project
Bash
uvicorn app:app --reload
Server starts at:

http://127.0.0.1:8000
📱 WhatsApp Integration Setup
1️⃣ Create Twilio Account
Use: twilio.com⁠�
2️⃣ Activate WhatsApp Sandbox
Send:

join your-code
to Twilio WhatsApp sandbox number.
3️⃣ Set Webhook URL
Example:

https://your-ngrok-url.ngrok-free.app/whatsapp
Set it inside Twilio Sandbox webhook settings.
🌍 Example WhatsApp Flow
User:

Garbage near my house
Bot:

📍 Please send your location using Google Maps link

Example:
https://maps.google.com/?q=17.3850,78.4867
User:
Sends Google Maps location
Bot:

✅ Complaint Registered
ID: C12345
Category: Garbage
🧠 Machine Learning
The project uses:
TF-IDF Vectorizer
Naive Bayes Classifier
Model files:

models/model.pkl
models/vectorizer.pkl
