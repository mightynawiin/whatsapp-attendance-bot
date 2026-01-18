from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import threading
import os
import pandas as pd
from scraper import get_attendance_data

load_dotenv()

app = Flask(__name__)

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def find_column(df, keyword):
    for col in df.columns:
        if keyword.lower() in col.lower():
            return col
    return None

def process_and_send(reg_no, password, sender):
    try:
        print("🟡 Background thread started")

        df, error = get_attendance_data(reg_no, password)

        if error:
            message = f"❌ Attendance fetch failed:\n{error}"

        elif df is None or df.empty:
            message = "⚠️ Login successful but no attendance data found."

        else:
            subject_col = find_column(df, "subject")
            attendance_col = find_column(df, "attendance")

            if not subject_col or not attendance_col:
                message = f"⚠️ Data format changed.\nColumns found: {list(df.columns)}"
            else:
                details = "\n".join(
                    [f"{row[subject_col]} : {row[attendance_col]}%"
                     for _, row in df.iterrows()]
                )
                avg = round(df[attendance_col].mean(), 2)

                message = (
                    f"✅ *Attendance Report*\n"
                    f"---------------------\n"
                    f"{details}\n"
                    f"---------------------\n"
                    f"📊 *Average*: {avg}%"
                )

        print("🟢 Sending WhatsApp message now")

        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=sender,
            body=message
        )

        print("✅ Message sent")

    except Exception as e:
        print("🔴 Fatal background error:", e)



@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming = request.values.get("Body", "").strip()
    sender = request.values.get("From")

    resp = MessagingResponse()
    msg = resp.message()

    if " " not in incoming:
        msg.body("⚠️ Send credentials like:\n`REGNO PASSWORD`")
        return str(resp)

    reg_no, password = incoming.split(" ", 1)

    threading.Thread(
        target=process_and_send,
        args=(reg_no, password, sender)
    ).start()

    msg.body("⏳ Fetching your attendance, please wait...")
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
