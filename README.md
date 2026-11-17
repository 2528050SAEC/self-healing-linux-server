# Self-Healing Linux Server Web App

Academic project: a Flask dashboard monitors a Linux systemd service and demonstrates automatic recovery.

## Features
- Live CPU, RAM and disk monitoring
- Linux service status
- Self-healing Bash monitor
- Automatic service restart
- Recovery log
- Browser dashboard
- Demo failure/recovery buttons

## 1. Install on Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-venv nginx
sudo systemctl enable --now nginx

cd self_healing_linux_server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Run the web dashboard

```bash
python3 app.py
```

Open:
`http://localhost:5000`

## 3. Allow the demo buttons to run systemctl

Create a sudoers rule:

```bash
sudo visudo
```

Add a rule appropriate to your Linux username, for example:

```text
YOUR_USERNAME ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop nginx, /usr/bin/systemctl restart nginx
```

Replace `YOUR_USERNAME`.

The Bash self-healing monitor itself should be run with suitable privileges:

```bash
sudo SERVICE=nginx CHECK_INTERVAL=10 ./scripts/self_heal.sh
```

## 4. Demonstrate self-healing

Terminal 1:

```bash
sudo SERVICE=nginx CHECK_INTERVAL=5 ./scripts/self_heal.sh
```

Terminal 2:

```bash
sudo systemctl stop nginx
```

Within the next check interval, the monitor detects the failure and restarts nginx.

Then refresh the dashboard. The log will show:
- failure detected
- recovery attempted
- recovery success

## Optional systemd installation

Copy the project to `/opt/self-healing-linux-server`, then:

```bash
sudo cp systemd/self-healing-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now self-healing-monitor
sudo systemctl status self-healing-monitor
```

## Important
This project is designed for a controlled academic demo. Do not give the web app unrestricted shell access. Keep the allowed service fixed and use least-privilege sudo rules.
