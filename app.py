
from flask import Flask, render_template, jsonify
from pathlib import Path
import subprocess, time, re
import psutil

app = Flask(__name__)
BASE = Path(__file__).resolve().parent
LOG_FILE = BASE / "logs" / "self_healing.log"

# Change this to another Linux service if required.
MONITORED_SERVICE = "nginx"

def service_status(service=MONITORED_SERVICE):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True, text=True, timeout=3
        )
        status = result.stdout.strip()
        return status if status else "unknown"
    except Exception as e:
        return "unavailable"

def recent_logs(limit=12):
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text(errors="ignore").splitlines()
    return lines[-limit:][::-1]

def system_data():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "cpu": round(psutil.cpu_percent(interval=0.2), 1),
        "memory": round(mem.percent, 1),
        "disk": round(disk.percent, 1),
        "uptime": int(time.time() - psutil.boot_time())
    }

@app.route("/")
def index():
    return render_template("index.html", service=MONITORED_SERVICE)

@app.route("/api/status")
def api_status():
    return jsonify({
        "service": MONITORED_SERVICE,
        "service_status": service_status(),
        "system": system_data(),
        "logs": recent_logs()
    })

@app.post("/api/demo-failure")
def demo_failure():
    # This is intentionally limited to the configured service.
    # It is useful for a classroom demonstration.
    try:
        result = subprocess.run(
            ["sudo", "systemctl", "stop", MONITORED_SERVICE],
            capture_output=True, text=True, timeout=10
        )
        return jsonify({"ok": result.returncode == 0, "message": "Demo failure requested."})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)}), 500

@app.post("/api/recover")
def recover():
    try:
        result = subprocess.run(
            ["sudo", "systemctl", "restart", MONITORED_SERVICE],
            capture_output=True, text=True, timeout=10
        )
        return jsonify({
            "ok": result.returncode == 0,
            "message": "Recovery requested.",
            "detail": result.stderr.strip()
        })
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
