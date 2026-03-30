from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3, os, datetime

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

DB = os.path.join(os.path.dirname(__file__), "tourismict.db")

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        brand TEXT,
        model TEXT,
        serial_number TEXT,
        location TEXT,
        assigned_to TEXT,
        status TEXT DEFAULT 'Active',
        purchase_date TEXT,
        purchase_cost REAL,
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS software (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        vendor TEXT,
        version TEXT,
        license_key TEXT,
        license_type TEXT,
        seats INTEGER DEFAULT 1,
        installed_on TEXT,
        purchase_date TEXT,
        expiry_date TEXT,
        cost REAL,
        status TEXT DEFAULT 'Active',
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        submitted_by TEXT NOT NULL,
        priority TEXT DEFAULT 'Medium',
        status TEXT DEFAULT 'Open',
        category TEXT,
        assigned_to TEXT,
        resolution TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now')),
        resolved_at TEXT
    );

    CREATE TABLE IF NOT EXISTS network_devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ip_address TEXT,
        mac_address TEXT,
        device_type TEXT,
        location TEXT,
        status TEXT DEFAULT 'Online',
        last_seen TEXT DEFAULT (datetime('now')),
        notes TEXT
    );
    """)

    # Seed sample data if empty
    if c.execute("SELECT COUNT(*) FROM assets").fetchone()[0] == 0:
        assets = [
            ("Dell OptiPlex 7090", "Desktop", "Dell", "OptiPlex 7090", "SN-MOT-001", "Finance Office", "Sione Taufa", "Active", "2023-01-15", 1200.00, "Main workstation"),
            ("HP LaserJet Pro", "Printer", "HP", "LaserJet Pro M404dn", "SN-MOT-002", "Reception", "Shared", "Active", "2022-06-10", 450.00, "Network printer"),
            ("Cisco Switch 24-port", "Network", "Cisco", "Catalyst 2960", "SN-MOT-003", "Server Room", "IT", "Active", "2021-03-20", 1800.00, "Core switch"),
            ("Dell PowerEdge R340", "Server", "Dell", "PowerEdge R340", "SN-MOT-004", "Server Room", "IT", "Active", "2021-03-20", 4500.00, "Primary file server"),
            ("Lenovo ThinkPad E14", "Laptop", "Lenovo", "ThinkPad E14", "SN-MOT-005", "Tourism Division", "Ana Fifita", "Active", "2023-08-01", 980.00, ""),
            ("HP EliteBook 840", "Laptop", "HP", "EliteBook 840 G8", "SN-MOT-006", "Support Services", "Mele Tonga", "Under Repair", "2022-02-14", 1100.00, "Keyboard issue"),
            ("APC UPS 1500VA", "UPS", "APC", "Smart-UPS 1500", "SN-MOT-007", "Server Room", "IT", "Active", "2021-03-20", 600.00, "Backup power"),
            ("Canon EOS R50", "Camera", "Canon", "EOS R50", "SN-MOT-008", "Media Unit", "Tevita Lolo", "Active", "2023-11-05", 850.00, "Tourism media"),
        ]
        c.executemany("INSERT INTO assets (name,type,brand,model,serial_number,location,assigned_to,status,purchase_date,purchase_cost,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)", assets)

    if c.execute("SELECT COUNT(*) FROM software").fetchone()[0] == 0:
        software = [
            ("Microsoft Office 365", "Microsoft", "2021", "XXXXX-XXXXX-00001", "Subscription", 20, "All workstations", "2023-01-01", "2025-01-01", 2400.00, "Active", "Annual renewal"),
            ("Kaspersky Endpoint Security", "Kaspersky", "11.0", "XXXXX-XXXXX-00002", "Subscription", 15, "All workstations", "2023-06-01", "2024-06-01", 750.00, "Active", ""),
            ("Adobe Acrobat Pro", "Adobe", "2023", "XXXXX-XXXXX-00003", "Perpetual", 3, "Finance, HR, IT", "2022-09-01", None, 420.00, "Active", ""),
            ("Sage Accounting", "Sage", "50", "XXXXX-XXXXX-00004", "Subscription", 2, "Finance", "2022-01-01", "2024-01-01", 1200.00, "Expired", "Renewal pending"),
            ("Adobe Premiere Pro", "Adobe", "2023", "XXXXX-XXXXX-00005", "Subscription", 1, "Media Unit", "2023-11-01", "2024-11-01", 660.00, "Active", "Video editing"),
            ("Zoom Business", "Zoom", "5.x", "XXXXX-XXXXX-00006", "Subscription", 10, "All staff", "2023-03-01", "2025-03-01", 1800.00, "Active", ""),
        ]
        c.executemany("INSERT INTO software (name,vendor,version,license_key,license_type,seats,installed_on,purchase_date,expiry_date,cost,status,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", software)

    if c.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 0:
        tickets = [
            ("Computer running very slow", "My desktop takes 10+ minutes to boot. Started 3 days ago.", "Sione Taufa", "High", "Open", "Hardware", "Samiuela Taukafa", None),
            ("Cannot access shared drive", "Getting 'Access Denied' when opening the Z: drive.", "Ana Fifita", "High", "In Progress", "Network", "Samiuela Taukafa", None),
            ("Printer not printing", "HP printer in reception shows offline but is turned on.", "Mele Tonga", "Medium", "Open", "Hardware", None, None),
            ("Email signature update needed", "Please update my email signature to new title.", "Tevita Lolo", "Low", "Resolved", "Software", "Samiuela Taukafa", "Updated in Outlook settings"),
            ("Website login issue", "Cannot login to the tourism portal since password reset.", "Lupe Vaka", "Medium", "Resolved", "Software", "Samiuela Taukafa", "Cleared browser cache, reset credentials"),
            ("New staff laptop setup", "New staff member starting Monday needs laptop configured.", "HR Division", "High", "Open", "Setup", None, None),
        ]
        c.executemany("INSERT INTO tickets (title,description,submitted_by,priority,status,category,assigned_to,resolution) VALUES (?,?,?,?,?,?,?,?)", tickets)

    if c.execute("SELECT COUNT(*) FROM network_devices").fetchone()[0] == 0:
        devices = [
            ("MOT-ROUTER-01", "192.168.1.1", "AA:BB:CC:DD:EE:01", "Router", "Server Room", "Online"),
            ("MOT-SWITCH-01", "192.168.1.2", "AA:BB:CC:DD:EE:02", "Switch", "Server Room", "Online"),
            ("MOT-SERVER-01", "192.168.1.10", "AA:BB:CC:DD:EE:03", "Server", "Server Room", "Online"),
            ("MOT-AP-FLOOR1", "192.168.1.20", "AA:BB:CC:DD:EE:04", "Access Point", "Ground Floor", "Online"),
            ("MOT-AP-FLOOR2", "192.168.1.21", "AA:BB:CC:DD:EE:05", "Access Point", "First Floor", "Online"),
            ("MOT-PRINTER-01", "192.168.1.30", "AA:BB:CC:DD:EE:06", "Printer", "Reception", "Offline"),
            ("MOT-PC-FIN01", "192.168.1.50", "AA:BB:CC:DD:EE:07", "Workstation", "Finance Office", "Online"),
            ("MOT-PC-FIN02", "192.168.1.51", "AA:BB:CC:DD:EE:08", "Workstation", "Finance Office", "Online"),
            ("MOT-PC-TOUR01", "192.168.1.60", "AA:BB:CC:DD:EE:09", "Workstation", "Tourism Division", "Online"),
            ("MOT-NAS-01", "192.168.1.15", "AA:BB:CC:DD:EE:0A", "NAS Storage", "Server Room", "Online"),
        ]
        c.executemany("INSERT INTO network_devices (name,ip_address,mac_address,device_type,location,status) VALUES (?,?,?,?,?,?)", devices)

    conn.commit()
    conn.close()

# ── DASHBOARD ──────────────────────────────────────────
@app.route("/api/dashboard")
def dashboard():
    conn = get_db()
    c = conn.cursor()
    total_assets = c.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
    active_assets = c.execute("SELECT COUNT(*) FROM assets WHERE status='Active'").fetchone()[0]
    repair_assets = c.execute("SELECT COUNT(*) FROM assets WHERE status='Under Repair'").fetchone()[0]
    retired_assets = c.execute("SELECT COUNT(*) FROM assets WHERE status='Retired'").fetchone()[0]
    total_software = c.execute("SELECT COUNT(*) FROM software").fetchone()[0]
    expiring_software = c.execute("SELECT COUNT(*) FROM software WHERE expiry_date IS NOT NULL AND expiry_date <= date('now', '+60 days') AND status='Active'").fetchone()[0]
    expired_software = c.execute("SELECT COUNT(*) FROM software WHERE status='Expired'").fetchone()[0]
    open_tickets = c.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'").fetchone()[0]
    inprog_tickets = c.execute("SELECT COUNT(*) FROM tickets WHERE status='In Progress'").fetchone()[0]
    resolved_tickets = c.execute("SELECT COUNT(*) FROM tickets WHERE status='Resolved'").fetchone()[0]
    online_devices = c.execute("SELECT COUNT(*) FROM network_devices WHERE status='Online'").fetchone()[0]
    offline_devices = c.execute("SELECT COUNT(*) FROM network_devices WHERE status='Offline'").fetchone()[0]
    asset_value = c.execute("SELECT COALESCE(SUM(purchase_cost),0) FROM assets").fetchone()[0]
    software_cost = c.execute("SELECT COALESCE(SUM(cost),0) FROM software").fetchone()[0]
    asset_types = [dict(r) for r in c.execute("SELECT type, COUNT(*) as count FROM assets GROUP BY type ORDER BY count DESC").fetchall()]
    recent_tickets = [dict(r) for r in c.execute("SELECT id,title,submitted_by,priority,status,created_at FROM tickets ORDER BY created_at DESC LIMIT 5").fetchall()]
    conn.close()
    return jsonify({
        "assets": {"total": total_assets, "active": active_assets, "repair": repair_assets, "retired": retired_assets, "value": round(asset_value, 2)},
        "software": {"total": total_software, "expiring": expiring_software, "expired": expired_software, "cost": round(software_cost, 2)},
        "tickets": {"open": open_tickets, "inprogress": inprog_tickets, "resolved": resolved_tickets},
        "network": {"online": online_devices, "offline": offline_devices, "total": online_devices + offline_devices},
        "asset_types": asset_types,
        "recent_tickets": recent_tickets
    })

# ── ASSETS ─────────────────────────────────────────────
@app.route("/api/assets", methods=["GET"])
def get_assets():
    conn = get_db()
    rows = conn.execute("SELECT * FROM assets ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/assets", methods=["POST"])
def create_asset():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO assets (name,type,brand,model,serial_number,location,assigned_to,status,purchase_date,purchase_cost,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (d.get("name"), d.get("type"), d.get("brand"), d.get("model"), d.get("serial_number"), d.get("location"), d.get("assigned_to"), d.get("status","Active"), d.get("purchase_date"), d.get("purchase_cost"), d.get("notes")))
    conn.commit(); conn.close()
    return jsonify({"success": True}), 201

@app.route("/api/assets/<int:aid>", methods=["PUT"])
def update_asset(aid):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE assets SET name=?,type=?,brand=?,model=?,serial_number=?,location=?,assigned_to=?,status=?,purchase_date=?,purchase_cost=?,notes=? WHERE id=?",
        (d.get("name"), d.get("type"), d.get("brand"), d.get("model"), d.get("serial_number"), d.get("location"), d.get("assigned_to"), d.get("status"), d.get("purchase_date"), d.get("purchase_cost"), d.get("notes"), aid))
    conn.commit(); conn.close()
    return jsonify({"success": True})

@app.route("/api/assets/<int:aid>", methods=["DELETE"])
def delete_asset(aid):
    conn = get_db()
    conn.execute("DELETE FROM assets WHERE id=?", (aid,))
    conn.commit(); conn.close()
    return jsonify({"success": True})

# ── SOFTWARE ───────────────────────────────────────────
@app.route("/api/software", methods=["GET"])
def get_software():
    conn = get_db()
    rows = conn.execute("SELECT * FROM software ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/software", methods=["POST"])
def create_software():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO software (name,vendor,version,license_key,license_type,seats,installed_on,purchase_date,expiry_date,cost,status,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (d.get("name"), d.get("vendor"), d.get("version"), d.get("license_key"), d.get("license_type"), d.get("seats",1), d.get("installed_on"), d.get("purchase_date"), d.get("expiry_date"), d.get("cost"), d.get("status","Active"), d.get("notes")))
    conn.commit(); conn.close()
    return jsonify({"success": True}), 201

@app.route("/api/software/<int:sid>", methods=["PUT"])
def update_software(sid):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE software SET name=?,vendor=?,version=?,license_key=?,license_type=?,seats=?,installed_on=?,purchase_date=?,expiry_date=?,cost=?,status=?,notes=? WHERE id=?",
        (d.get("name"), d.get("vendor"), d.get("version"), d.get("license_key"), d.get("license_type"), d.get("seats"), d.get("installed_on"), d.get("purchase_date"), d.get("expiry_date"), d.get("cost"), d.get("status"), d.get("notes"), sid))
    conn.commit(); conn.close()
    return jsonify({"success": True})

@app.route("/api/software/<int:sid>", methods=["DELETE"])
def delete_software(sid):
    conn = get_db()
    conn.execute("DELETE FROM software WHERE id=?", (sid,))
    conn.commit(); conn.close()
    return jsonify({"success": True})

# ── TICKETS ────────────────────────────────────────────
@app.route("/api/tickets", methods=["GET"])
def get_tickets():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tickets ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/tickets", methods=["POST"])
def create_ticket():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO tickets (title,description,submitted_by,priority,status,category,assigned_to,resolution) VALUES (?,?,?,?,?,?,?,?)",
        (d.get("title"), d.get("description"), d.get("submitted_by"), d.get("priority","Medium"), d.get("status","Open"), d.get("category"), d.get("assigned_to"), d.get("resolution")))
    conn.commit(); conn.close()
    return jsonify({"success": True}), 201

@app.route("/api/tickets/<int:tid>", methods=["PUT"])
def update_ticket(tid):
    d = request.json
    resolved_at = datetime.datetime.now().isoformat() if d.get("status") == "Resolved" else None
    conn = get_db()
    conn.execute("UPDATE tickets SET title=?,description=?,submitted_by=?,priority=?,status=?,category=?,assigned_to=?,resolution=?,updated_at=datetime('now'),resolved_at=COALESCE(?,resolved_at) WHERE id=?",
        (d.get("title"), d.get("description"), d.get("submitted_by"), d.get("priority"), d.get("status"), d.get("category"), d.get("assigned_to"), d.get("resolution"), resolved_at, tid))
    conn.commit(); conn.close()
    return jsonify({"success": True})

@app.route("/api/tickets/<int:tid>", methods=["DELETE"])
def delete_ticket(tid):
    conn = get_db()
    conn.execute("DELETE FROM tickets WHERE id=?", (tid,))
    conn.commit(); conn.close()
    return jsonify({"success": True})

# ── NETWORK ────────────────────────────────────────────
@app.route("/api/network", methods=["GET"])
def get_network():
    conn = get_db()
    rows = conn.execute("SELECT * FROM network_devices ORDER BY device_type, name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/network", methods=["POST"])
def create_network():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO network_devices (name,ip_address,mac_address,device_type,location,status,notes) VALUES (?,?,?,?,?,?,?)",
        (d.get("name"), d.get("ip_address"), d.get("mac_address"), d.get("device_type"), d.get("location"), d.get("status","Online"), d.get("notes")))
    conn.commit(); conn.close()
    return jsonify({"success": True}), 201

@app.route("/api/network/<int:nid>", methods=["PUT"])
def update_network(nid):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE network_devices SET name=?,ip_address=?,mac_address=?,device_type=?,location=?,status=?,notes=?,last_seen=datetime('now') WHERE id=?",
        (d.get("name"), d.get("ip_address"), d.get("mac_address"), d.get("device_type"), d.get("location"), d.get("status"), d.get("notes"), nid))
    conn.commit(); conn.close()
    return jsonify({"success": True})

@app.route("/api/network/<int:nid>", methods=["DELETE"])
def delete_network(nid):
    conn = get_db()
    conn.execute("DELETE FROM network_devices WHERE id=?", (nid,))
    conn.commit(); conn.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
else:
    init_db()
