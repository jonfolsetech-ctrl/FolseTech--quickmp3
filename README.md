# QuickMP3 – FolseTech AI Solutions Edition

A branded demo app by **FolseTech AI Solutions** (River Parishes, LA) for turning lyrics into AI-generated songs.

This project showcases:

- 🎧 FastAPI backend
- 🎚 Stubbed AI pipeline (instrumental + vocals + mixing using pydub)
- 🎛 React frontend with FolseTech-branded UI

> ⚠️ Note: The AI parts are *stubbed*. You can wire in real services like Suno, Udio, ElevenLabs, or RVC where indicated in `backend/main.py`.

---

## ✅ Requirements

- Python 3.10+
- Node.js 18+
- ffmpeg installed on your system (required by `pydub`)

---

## 🖥 Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The UI is branded:

- App name: **QuickMP3 by FolseTech AI Solutions**
- Tagline: *"Transforming ideas into intelligent tracks."*
- Colors inspired by FolseTech’s tech blue / teal palette.

You can deploy:

- Frontend → Vercel / Netlify / Amplify
- Backend → Render, Railway, EC2, etc.

---

## 🔌 Wiring Real AI Providers

Inside `backend/main.py`, replace:

- `generate_instrumental()` → Call Suno/Udio/music model API
- `synthesize_vocals()` → Call ElevenLabs / RVC / other voice cloning API

Then keep `mix_tracks()` as your final combiner, or replace with a DAW-style mixer.
