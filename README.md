# TourismICT — Ministry of Tourism ICT Management Portal

A full-stack ICT asset and systems management portal built for the **Ministry of Tourism, Kingdom of Tonga**.

## Modules

| Module | Description |
|---|---|
| Dashboard | Live overview: asset counts, ticket status, software alerts, network health |
| ICT Asset Register | Track all hardware — desktops, laptops, servers, printers, cameras |
| Software Inventory | Manage licenses, versions, seat counts, expiry alerts |
| Helpdesk Tickets | Log and resolve staff IT issues with priority and audit trail |
| Network Monitor | Register and monitor all network devices and connectivity status |

## Tech Stack

- **Backend**: Python / Flask + SQLite
- **Frontend**: React (CDN, no build step)
- **Deployment**: Render.com (free tier)

---

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/tourismict.git
cd tourismict
```

### 2. Start the backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs at: `http://localhost:5000`

### 3. Open the frontend
Open `frontend/index.html` directly in your browser.

> The frontend connects to `http://localhost:5000/api` by default.

---

## Deploy to Render (Live URL)

### Backend (Web Service)
1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo
3. Set:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Deploy — note your URL e.g. `https://tourismict-backend.onrender.com`

### Frontend (Static Site)
1. Open `frontend/index.html`
2. Change line: `const API = "http://localhost:5000/api";`
   to: `const API = "https://tourismict-backend.onrender.com/api";`
3. In Render → New → Static Site
4. Set **Publish Directory** to `frontend`
5. Deploy

---

## Project Structure

```
tourismict/
├── backend/
│   ├── app.py            # Flask API (all routes + SQLite DB)
│   ├── requirements.txt  # Python dependencies
│   └── tourismict.db     # Auto-created SQLite database
├── frontend/
│   └── index.html        # Full React app (single file)
├── render.yaml           # Render deployment config
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/dashboard | Summary stats for dashboard |
| GET/POST | /api/assets | List / create assets |
| PUT/DELETE | /api/assets/:id | Update / delete asset |
| GET/POST | /api/software | List / create software |
| PUT/DELETE | /api/software/:id | Update / delete software |
| GET/POST | /api/tickets | List / create tickets |
| PUT/DELETE | /api/tickets/:id | Update / delete ticket |
| GET/POST | /api/network | List / create network devices |
| PUT/DELETE | /api/network/:id | Update / delete network device |

---

Built by **Samiuela Taukafa** — portfolio project for Senior Computer Programmer/Media application, Ministry of Tourism, 2026.
