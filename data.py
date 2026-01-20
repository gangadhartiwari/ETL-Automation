import requests
import json
from datetime import datetime, timedelta

API_URL = "http://corporate.margerp.com/api/eOnlineData/MargCorporateEDE"

STATE_FILE = r"C:/Users/synchem/Desktop/MargtoSQL/last_run.json"

# --- Read last run datetime ---
try:
    with open(STATE_FILE, "r") as f:
        last_run = json.load(f).get("Datetime", "")
except FileNotFoundError:
    last_run = ""

payload = {
    "CompanyCode": "SynchemPharmace3",
    "Datetime": last_run,
    "MargKey": "F98OMVZ5I47IKM1B1QZ1ITTTM9H1IQC5SIRN",
    "Index": 0,
    "CompanyID": "10641",
    "APIType": "1"
}

try:
    response = requests.post(API_URL, json=payload, timeout=120)
    response.raise_for_status()  # Raise error if status != 200

    long_data_string = response.text.strip().strip('"')  # Clean string

    # Save to file
    with open(r"C:/Users/synchem/Desktop/MargtoSQL/api_response.txt", "w", encoding="utf-8") as f:
        f.write(long_data_string)

    print(" API data saved, length:", len(long_data_string))
    # ✅ Update last run AFTER successful fetch
    new_run_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    with open(STATE_FILE, "w") as f:
        json.dump({"Datetime": new_run_time}, f)

    print(" Last run updated:", new_run_time)

except Exception as e:
    print(" API call failed:", e)
