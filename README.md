
```markdown
# 🌐 Network Monitoring Dashboard

An interactive local network monitoring web application built with Python (Flask) that provides real-time tracking, device status classification, and management capabilities.

## 🚀 Features
- **Real-time Network Scanning:** Scans the local network quickly using multi-threading (`ThreadPoolExecutor`) to discover active devices.
- **Device Recognition:** Automatically identifies and categorizes devices (Apple, Samsung, Laptops, IoT/Routers) with custom icons.
- **Status Tracking:** Tracks whether devices are **Online** or **Offline** along with their last-seen timestamp.
- **Interactive Dashboard:** Built with a modern UI, featuring a dynamic status chart (Chart.js), live search filter, and quick management options.
- **Data Export:** Export current network device reports directly to a **CSV** file.
- **Device Management:** Easily delete specific devices or clear the entire device list with a single click.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, JSON
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Networking:** Socket, Subprocess (ARP & Ping)

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/muhammedHammad555/Network-Monitoring-Dashboard.git](https://github.com/muhammedHammad555/Network-Monitoring-Dashboard.git)

```

2. **Navigate to the project folder:**
```bash
cd Network-Monitoring-Dashboard

```


3. **Install dependencies (Flask):**
```bash
pip install flask

```


4. **Run the application:**
* On Windows, simply double-click the **`run.bat`** file.


* Or run it via terminal:



```bash
python app.py

```

5. **Access the Dashboard:**
Open your browser and navigate to: `http://127.0.0.1:5000`

```

```
