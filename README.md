# 📸 The Absentee — AI-Powered Attendance System

**The Absentee** (AI-Attendance-App) is a smart classroom attendance system that uses **face recognition** and **voice recognition** to mark attendance automatically — no more manual roll calls or proxy attendance.

Built with **Streamlit**, powered by **Supabase**, and driven by **AI/ML** models for biometric verification.

---

## ✨ Features

- 🧑‍🏫 **Teacher Dashboard** — create subjects, generate enrollment links/QR codes, and manage class rosters
- 🎓 **Student Portal** — enroll into subjects via shareable links, mark attendance using face/voice verification
- 🔍 **Face Recognition** — automatic identity verification using `face_recognition` + `dlib`
- 🎙️ **Voice Recognition** — secondary/alternate verification using `resemblyzer` + `librosa`
- 🔗 **QR Code / Link-based Enrollment** — students join subjects instantly via a shared link or scannable QR code (`segno`)
- ☁️ **Cloud Backend** — attendance records, user data, and subjects stored securely via **Supabase**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| Face Recognition | `face_recognition`, `dlib-bin` |
| Voice Recognition | `resemblyzer`, `librosa` |
| Data Handling | `numpy`, `pandas`, `scikit-learn` |
| Backend / Database | [Supabase](https://supabase.com/) |
| QR Code Generation | `segno` |
| Image Processing | `Pillow` |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/snehal-k04/AI-Attendance-App.git
cd AI-Attendance-App
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Supabase credentials
Create a `.streamlit/secrets.toml` file in the project root with your Supabase project details:
```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-anon-key"
```
> ⚠️ This file is git-ignored by default — never commit your actual credentials.

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
snapclass/
├── app.py                     # App entry point
├── requirements.txt
├── src/
│   ├── components/            # Reusable UI components (dialogs, cards, header/footer)
│   ├── database/               # Supabase connection & queries
│   ├── pipeline/               # Face & voice recognition pipelines
│   ├── screens/                # Home, Teacher, and Student screens
│   └── ui/                     # Layout & styling
```

---

## 👥 User Roles

- **Teacher**: Creates subjects, shares enrollment links/QR codes, monitors attendance
- **Student**: Enrolls via link, registers face/voice, marks attendance in class

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/snehal-k04/AI-Attendance-App/issues).

---
