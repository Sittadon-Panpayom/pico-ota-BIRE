# main.py

import machine
import urequests as requests
import json
import time
from picozero import RGBLED
rgb = RGBLED(red = 16, green = 17, blue = 18,active_high=False) 

# === CONFIG ===
RAW_VERSION_URL = "https://raw.githubusercontent.com/Sittadon-Panpayom/pico-ota-BIRE/refs/heads/main/version.json"
RAW_MAIN_URL    = "https://raw.githubusercontent.com/Sittadon-Panpayom/pico-ota-BIRE/refs/heads/main/main.py"
CHECK_INTERVAL = 10  # seconds

# === Blink Setup ===
led = machine.Pin("LED", machine.Pin.OUT)

def blink(n=1, delay=10):
    print(f"Blinking {n} times with {delay}s delay.")
    for _ in range(n):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)

# === Version Handling ===
def get_local_version():
    print("Fetching local version...")
    try:
        with open("local_version.json") as f:
            local_data = json.load(f)
            version = local_data.get("version", "0.0.0")
            print(f"Local version: {version}")
            return version
    except Exception as e:
        print(f"Error reading local_version.json: {e}")
        return "0.0.0"

def get_remote_version():
    print(f"Fetching remote version from: {RAW_VERSION_URL}")
    try:
        res = requests.get(RAW_VERSION_URL)
        print(f"Response Status Code: {res.status_code}")
        if res.status_code == 200:
            data = res.json()  # Parse JSON response
            version = data.get("version", "0.0.0")
            print(f"Remote version: {version}")
            return version
        else:
            print(f"Error: Received non-200 status code {res.status_code}")
    except Exception as e:
        print(f"Error getting remote version: {e}")
    return "0.0.0"

def update_code():
    print("Attempting to update main.py...")
    try:
        res = requests.get(RAW_MAIN_URL)
        print(f"Response Status Code for main.py: {res.status_code}")
        if res.status_code == 200:
            with open("main.py", "w") as f:
                f.write(res.text)
            print("main.py saved.")
        else:
            print(f"Error: Received non-200 status code {res.status_code} while fetching main.py")

        # Fetch and save the new version info
        res = requests.get(RAW_VERSION_URL)
        print(f"Response Status Code for version.json: {res.status_code}")
        if res.status_code == 200:
            with open("local_version.json", "w") as f:
                f.write(res.text)
            print("Version updated.")
        else:
            print(f"Error: Received non-200 status code {res.status_code} while fetching version.json")

        print("Update successful, rebooting...")
        time.sleep(1)
        machine.reset()
    except Exception as e:
        print(f"Update failed: {e}")

# === Main Loop ===
while True:
    print("Starting the main loop...")    
    rgb.color = (0, 255,0 ) #blue
    time.sleep(5)
    rgb.color = (0,0,0) 
    local = get_local_version()
    remote = get_remote_version()
    print(f"Local version: {local}, Remote version: {remote}")
    if local != remote:
        print("Version mismatch detected, updating code...")
        update_code()
        rgb.cycle() #cycle through colour
        time.sleep(5)
    else:
        print("Versions are the same, no update required.")
        rgb.(255,0,0) #red
