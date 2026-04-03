# 📬 Urgent Email Viewer

A minimalist desktop application built with Python and PyQt5 to help you stay on top of **urgent or important emails** in your Gmail inbox over the past 30 days. 🧠⚡

---

## 🚀 Features

- 🔍 Scans your Gmail inbox for keywords like `urgent`, `asap`, `important`, `attention`, etc.
- 📆 Displays subject lines with formatted timestamps.
- 💬 Hover over truncated subjects to preview the full message title.
- 🔗 Click the `Visit` button to open the email in your browser, using the correct authenticated Gmail account.
- 🔄 Refresh manually or automatically every 60 seconds.
- ✨ Clean, simple UI with scrollable results.

---

## 🛠️ Setup Instructions

### 📋 Requirements

- 🐍 Make sure you have **Python 3.7+** installed.
- 👤 A Google account to create API credentials.

---

### 🐙 Step 1: Clone or download the repository

```bash
git clone https://github.com/connerTeev/Urgent-Gmail-Viewer.git
cd urgent-email-viewer
```

---

### ☁️ Step 2: Create a Google Cloud Project and enable Gmail API

- 🌐 Visit the Google Cloud Console.

- ➕ Create a new project or select an existing one.

- 📚 In the sidebar, go to APIs & Services > Library.

- 🔎 Search for Gmail API and click Enable.

---

### 🔐 Step 3: Create OAuth 2.0 Credentials

- 🛠️ In the Cloud Console, go to APIs & Services > Credentials.

- ➕ Click Create Credentials > OAuth client ID.

- 💻 Select Desktop app as the application type.

- 🏷️ Give it a name, then click Create.

- ⬇️ Download the resulting credentials.json file.

- 📂 Place the credentials.json file in the root directory of this project (same folder as the Python script).

---

### 📦 Step 4: Install Python dependencies

```bash
pip install --upgrade google-auth google-auth-oauthlib google-api-python-client PyQt5
```

---

### ▶️ Step 5: Run the app

```bash
python urgent_gmail_viewer.py
```
