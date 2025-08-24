# -------------------------------------------------
# run.sh (optional helper for Linux/macOS)
# -------------------------------------------------
#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python create_db.py
python seed_admin.py
flask --app app.py --debug run --port 5000