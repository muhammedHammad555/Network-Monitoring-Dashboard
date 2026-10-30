import socket
import subprocess
import platform
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

DATA_FILE = "devices.json"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "192.168.1.1"
    finally:
        s.close()
    return ip

def ping_device(ip):
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "300", ip]
    else:
        command = ["ping", "-c", "1", "-W", "1", ip]

    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def get_mac_addresses():
    result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    macs = {}

    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            ip = parts[0]
            mac = parts[1].replace("-", ":").lower()
            if "." in ip and ":" in mac:
                macs[ip] = mac

    return macs

def get_device_name(ip, mac, old_devices):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        if hostname and hostname != ip:
            return hostname
    except:
        pass

    old_name = old_devices.get(ip, {}).get("name", "")
    if old_name and old_name != "Unknown Device":
        return old_name

    mac = mac.lower()

    if mac.startswith(("a4:", "f0:", "d0:", "bc:", "28:", "ac:", "f4:")):
        return "Apple Device"

    if mac.startswith(("dc:", "f8:", "3c:", "58:", "cc:", "b4:")):
        return "Samsung Device"

    if mac.startswith(("00:1a:", "b8:27:", "c8:", "e8:")):
        return "Router / IoT Device"

    return "Unknown Device"

def get_device_icon(name, mac):
    text = (name + " " + mac).lower()

    if "iphone" in text or "apple" in text or "samsung" in text or "android" in text:
        return "📱"

    if "desktop" in text or "laptop" in text or "pc" in text or "hp" in text or "lenovo" in text or "dell" in text:
        return "💻"

    if "printer" in text:
        return "🖨️"

    if "router" in text or "iot" in text or "gateway" in text:
        return "📶"

    return "🖥️"

def get_device_type(mac):
    mac = mac.lower()

    # تحديد الأجهزة حسب MAC Address
    if mac.startswith(("00:1a:", "f0:", "a4:", "3c:", "58:", "b8:27:")):
        return "Apple Device"
    
    if mac.startswith(("dc:", "f8:", "3c:", "58:")):
        return "Samsung Device"

    if mac.startswith(("00:1a:", "b8:27:", "c8:", "e8:")):
        return "Router / IoT Device"

    if mac.startswith(("ac:", "f4:", "3c:", "b4:")):
        return "Laptop/PC"

    if mac.startswith(("f0:", "e0:", "a8:", "a4:")):
        return "Phone / Tablet"
    
    return "Unknown Device"

def load_old_devices():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_devices(devices):
    with open(DATA_FILE, "w") as file:
        json.dump(devices, file, indent=4)

def scan_network():
    old_devices = load_old_devices()

    local_ip = get_local_ip()
    network_prefix = ".".join(local_ip.split(".")[:3])
    ips = [f"{network_prefix}.{i}" for i in range(1, 255)]

    with ThreadPoolExecutor(max_workers=80) as executor:
        results = list(executor.map(ping_device, ips))

    macs = get_mac_addresses()
    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    online_ips = []

    for ip, is_online in zip(ips, results):
        if is_online:
            online_ips.append(ip)

            is_new = ip not in old_devices

            mac = macs.get(ip, old_devices.get(ip, {}).get("mac", "Not Found"))
            device_name = get_device_name(ip, mac, old_devices)
            device_type = get_device_type(mac)
            icon = get_device_icon(device_name, mac)

            old_devices[ip] = {
                "name": device_name,
                "ip": ip,
                "mac": mac,
                "status": "Online",
                "last_seen": now,
                "icon": icon,
                "device_type": device_type,
                "is_new": is_new
            }

    for ip in old_devices:
        if ip not in online_ips:
            old_devices[ip]["status"] = "Offline"
            old_devices[ip]["is_new"] = False

    save_devices(old_devices)

    devices_list = list(old_devices.values())
    devices_list.sort(key=lambda x: x["status"] != "Online")

    return devices_list