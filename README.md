# Pico Weather API

A simple weather API using a Raspberry Pi Pico W and a DHT11 temperature and humidity sensor. This project provides real-time temperature, humidity, heat index, and dew point readings via a web server hosted on the Pico W.

## 🛠 Hardware Required
- Raspberry Pi Pico W
- DHT11 Temperature & Humidity Sensor
- Jumper Wires
- Breadboard

## 📚 Libraries Used
This project uses only built-in MicroPython libraries:
- `network` (for Wi-Fi connectivity)
- `socket` (for the web server)
- `dht` (for reading sensor data)
- `machine` (for GPIO control)
- `json` (for API response formatting)
- `time` (for delays)
- `ubinascii` (for MAC address formatting)

## 🚀 Installation
1. Install [Thonny](https://thonny.org/) on your computer.
2. Connect the Raspberry Pi Pico W to your PC via USB.
3. Open Thonny and install MicroPython on your Pico W if not already installed.
4. Copy the provided script (`main.py`) to your Pico W.
5. Modify the `SSID` and `PASSWORD` variables in the script to match your Wi-Fi credentials.
6. Save and run the script in Thonny.

## 🌐 API Usage
Once the Raspberry Pi Pico W connects to Wi-Fi, it starts a local web server. You can access the API using the assigned IP address or hostname:

- **URL Format:**
  - `http://<PICO_IP>` (e.g., `http://192.168.43.206`)
  - `http://pico-weather.local` (if mDNS is supported)

- **Example API Response:**
```json
{
  "ip": "http://192.168.43.206",
  "mac": "28:cd:c1:0f:f6:13",
  "temperature_C": 21,
  "temperature_F": 69.8,
  "humidity": 75,
  "heat_index_C": 22.46,
  "heat_index_F": 72.43,
  "dew_point_C": 33.83,
  "dew_point_F": 92.89,
  "hostname": "http://pico-weather.local"
}
```

## 🔗 Fetching Data via JavaScript
To fetch data from the API using JavaScript, you can use:
```js
fetch("http://192.168.43.206")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error("Error:", error));
```

## 💡 Notes
- Ensure your Pico W and the device accessing the API are on the same network.
- If accessing via hostname (`pico-weather.local`), mDNS must be supported by your system.
- Some browsers may block mixed-content HTTP requests if accessed from an HTTPS site.

Enjoy real-time weather data with your Pico W! 🌡️

