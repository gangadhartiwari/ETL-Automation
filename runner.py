import time
import traceback
from datetime import datetime
import subprocess
import os

# 🔒 FIXED paths 
PYTHON = r"C:\Users\synchem\AppData\Local\Programs\Python\Python311\python.exe"
BASE_DIR = r"C:\Users\synchem\Desktop\MargtoSQL"

SCRIPTS = [
    "data.py",
    "tojson.py",
    "tosql.py"
]

LOG_FILE = r"C:\Users\synchem\Desktop\MargtoSQL\python_service.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {msg}\n")

log("=== Python runner started ===")

while True:
    try:
        log("=== Job cycle started ===")

        for script in SCRIPTS:
            script_path = os.path.join(BASE_DIR, script)
            log(f"Running {script_path}")

            result = subprocess.run(
                [PYTHON, script_path],
                cwd=BASE_DIR,              # ⭐ IMPORTANT
                capture_output=True,
                text=True,
                timeout=300                # ⏱️ 5 min safety
            )

            if result.returncode != 0:
                log(f"ERROR in {script}")
                log("STDOUT:\n" + result.stdout)
                log("STDERR:\n" + result.stderr)
                break
            else:
                log(f"{script} completed successfully")

        log("=== Job cycle finished ===")

    except subprocess.TimeoutExpired:
        log("ERROR: Script timed out")

    except Exception:
        log("FATAL ERROR")
        log(traceback.format_exc())

    # 🔁 WAIT 30 MINUTES
    time.sleep(1800)
