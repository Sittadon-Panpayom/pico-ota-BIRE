#main.py

import machine
import urequests as requests
import json
import time

# === CONFIG ===
RAW_VERSION_URL = "https://github.com/Fayeinstainy/BIR25_TEAM_E/blob/pico-ota/version.json"
RAW_MAIN_URL    = "https://github.com/Fayeinstainy/BIR25_TEAM_E/edit/pico-ota/main.py"
CHECK_INTERVAL = 60  # seconds

# === Blink Setup ===
led = machine.Pin("LED", machine.Pin.OUT)

def blink(n=1, delay=0.1):
    for _ in range(n):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)

# === Version Handling ===
def get_local_version():
    try:
        with open("local_version.json") as f:
            return json.load(f).get("version", "0.0.0")
    except:
        return "0.0.0"

def get_remote_version():
    try:
        res = requests.get(RAW_VERSION_URL)
        if res.status_code == 200:
            return res.json().get("version", "0.0.0")
    except Exception as e:
        print("Error getting remote version:", e)
    return "0.0.0"

def update_code():
    try:
        print("Fetching updated main.py...")
        res = requests.get(RAW_MAIN_URL)
        if res.status_code == 200:
            with open("main.py", "w") as f:
                f.write(res.text)
            print("main.py saved.")

            # Save the new version
            res = requests.get(RAW_VERSION_URL)
            with open("local_version.json", "w") as f:
                f.write(res.text)

            print("Update successful, rebooting...")
            time.sleep(1)
            machine.reset()
    except Exception as e:
        print("Update failed:", e)

# === Main Loop ===
while True:
    #blink(1)
    for _ in range(CHECK_INTERVAL):
        blink(1, delay = 0.9)
        time.sleep(0.9)
    local = get_local_version()
    remote = get_remote_version()
    print(f"Local: {local}, Remote: {remote}")
    if local != remote:
        update_code()
