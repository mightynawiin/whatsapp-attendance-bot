  # 📱 WhatsApp Attendance Bot (Selenium-Based Automation)

A production-grade **WhatsApp bot** that securely fetches student attendance data from a college portal using **browser automation (Selenium)** and delivers a **real-time attendance report directly on WhatsApp**.

---

## 🚀 Project Overview

This project automates the complete flow of:

**WhatsApp Message → Secure Login → Attendance Scraping → Formatted Report → WhatsApp Reply**

It is designed to handle **JavaScript-heavy portals** where traditional API or request-based scraping is not possible.

---

## ✨ Key Features

* ✅ WhatsApp-based interaction (no UI needed)
* 🔐 Secure credential handling via environment variables
* 🤖 Selenium browser automation for JS-rendered portals
* ⚡ Non-blocking background processing using threading
* 📊 Clean, subject-wise attendance breakdown
* 📈 Automatic overall attendance calculation
* 🧩 Modular & maintainable code structure

---

## 🧠 Tech Stack

| Layer           | Technology              |
| --------------- | ----------------------- |
| Messaging       | Twilio WhatsApp Sandbox |
| Backend         | Flask (Python)          |
| Automation      | Selenium + ChromeDriver |
| Parsing         | Pandas                  |
| Async Handling  | Python Threading        |
| Environment     | python-dotenv           |
| Version Control | Git & GitHub            |

---

## 📂 Project Structure

```text
whatsapp-attendance-bot/
│
├── app.py              # Flask app + Twilio webhook
├── scraper.py          # Selenium attendance scraper
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignore secrets & cache
└── README.md           # Project documentation
```

---

## 🔄 System Flow (End-to-End)

### 🔁 High-Level Flowchart

```text
User (WhatsApp)
     |
     |  Roll No + Password
     ▼
Twilio WhatsApp Sandbox
     |
     |  Webhook (POST)
     ▼
Flask Application (app.py)
     |
     |  Start Background Thread
     ▼
Selenium Automation (scraper.py)
     |
     |  Login → Scrape Attendance
     ▼
Attendance Data Processing
     |
     |  Format Report
     ▼
Twilio API
     |
     ▼
User receives Attendance Report on WhatsApp
```

---

## 📱 WhatsApp Bot – Live Output

### ⏳ Initial Response

The bot immediately acknowledges the request to avoid timeouts.

*(Screenshot: Fetching attendance message)*

---

### ✅ Attendance Report

The final message includes:

* Subject-wise attendance
* Labs & internal sessions
* Overall average percentage

*(Screenshot: Detailed attendance report with average)*

> 📊 **Average Attendance Automatically Calculated**

---

## 🧪 Example WhatsApp Usage

### 📩 User Message

```text
23691A3294 Password
```

### 📤 Bot Response

```text
Attendance Report

23ENG101 : 80.0%
23MAT101 : 86.21%
23CSE101 : 87.3%
...
Average : 74.75%
```

---

## 🔐 Security Practices Followed

* ❌ No credentials stored in code
* ✅ Environment variables via `.env`
* ✅ `.env` excluded using `.gitignore`
* 🔄 Twilio Auth Token rotation recommended
* ⚠️ For educational/demo use only

---

## ⚙️ Local Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mightynawiin/whatsapp-attendance-bot.git
cd whatsapp-attendance-bot
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file:

```env
ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
PORT=5000
```

### 4️⃣ Run the Application

```bash
python app.py
```

### 5️⃣ Expose Locally (for Twilio)

```bash
ngrok http 5000
```

Update the Twilio Sandbox webhook:

```
https://<ngrok-id>.ngrok-free.app/whatsapp
```

---

## ⚠️ Limitations

* Requires Selenium (browser automation)
* Not suitable for serverless platforms
* Credentials are user-provided (educational use only)
* Portal UI changes may require scraper updates

---

## 🔮 Future Enhancements

* 🔐 OTP-based verification instead of passwords
* 🧵 Celery / Queue-based background jobs
* 🐳 Dockerized deployment
* 📊 PDF / Excel attendance export
* 📉 Low-attendance alerts
* ☁️ Migration to WhatsApp Cloud API

---

## 🧑‍💻 Author

**Naveen Bathini**
GitHub: [@mightynawiin](https://github.com/mightynawiin)

---

## 🏁 Final Note

This project demonstrates **real-world automation, backend engineering, async processing, and API integration**.

It is suitable for:

* 🎓 College projects
* 🧪 Proof-of-concept demos
* 💼 Resume & interviews

---

