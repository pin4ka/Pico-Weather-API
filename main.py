import network
import socket
import dht
import machine
import json
import time
import ubinascii

# Wi-Fi credentials (Change these)
SSID = "SSID"
PASSWORD = "PASSWORD"

# Custom hostname (set this to something unique)
HOSTNAME = "pico-weather"

# Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# LED setup
led = machine.Pin("LED", machine.Pin.OUT)

# LED indication functions
def led_fast_blink():
    for _ in range(2):
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)

def led_slow_blink():
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)

def led_fast_double_blink():
    for _ in range(2):
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
    time.sleep(0.2)

def led_fade_error():
    for i in range(0, 1024, 64):
        led.duty_u16(i)
        time.sleep(0.02)
    for i in range(1023, -1, -64):
        led.duty_u16(i)
        time.sleep(0.02)
    led.off()

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    led_fast_blink()
    time.sleep(0.5)

ip_address = wlan.ifconfig()[0]  # Get the assigned IP address
mac_address = ubinascii.hexlify(wlan.config('mac'), ':').decode()

print(f"Connected! IP: {ip_address}, MAC: {mac_address}")

# Set local hostname for easier access
network.hostname(HOSTNAME)

# DHT11 Sensor on GPIO 1
dht_sensor = dht.DHT11(machine.Pin(1))

# Function to calculate heat index (feels-like temperature)
def calculate_heat_index(temp, humidity):
    c1 = -8.78469475556
    c2 = 1.61139411
    c3 = 2.33854883889
    c4 = -0.14611605
    c5 = -0.012308094
    c6 = -0.0164248277778
    c7 = 0.002211732
    c8 = 0.00072546
    c9 = -0.000003582
    hi = c1 + (c2 * temp) + (c3 * humidity) + (c4 * temp * humidity) + (c5 * temp**2) + (c6 * humidity**2) + (c7 * temp**2 * humidity) + (c8 * temp * humidity**2) + (c9 * temp**2 * humidity**2)
    return round(hi, 2)

# Function to calculate dew point
def calculate_dew_point(temp, humidity):
    a, b = 17.27, 237.7
    alpha = ((a * temp) / (b + temp)) + (humidity / 100.0)
    dew_point = (b * alpha) / (a - alpha)
    return round(dew_point, 2)

# Start Web Server
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server = socket.socket()
    server.bind(addr)
    server.listen(5)
    print(f"Server running at http://{ip_address} or http://{HOSTNAME}.local")

    while True:
        client, addr = server.accept()
        print(f"Client connected from {addr}")
        request = client.recv(1024).decode()
        
        # Handle CORS Preflight Request
        if "OPTIONS" in request:
            response_headers = (
                "HTTP/1.1 204 No Content\r\n"
                "Access-Control-Allow-Origin: *\r\n"
                "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
                "Access-Control-Allow-Headers: Content-Type\r\n"
                "\r\n"
            )
            client.send(response_headers)
            client.close()
            continue

        try:
            led_fast_double_blink()  # Indicate data transfer
            
            dht_sensor.measure()
            temperature = dht_sensor.temperature()  # °C
            humidity = dht_sensor.humidity()  # %

            heat_index = calculate_heat_index(temperature, humidity)
            dew_point = calculate_dew_point(temperature, humidity)

            data = {
                "ip": f"http://{ip_address}",
                "hostname": f"http://{HOSTNAME}.local",
                "mac": mac_address,
                "temperature_C": temperature,
                "temperature_F": round(temperature * 9/5 + 32, 2),
                "humidity": humidity,
                "heat_index_C": heat_index,
                "heat_index_F": round(heat_index * 9/5 + 32, 2),
                "dew_point_C": dew_point,
                "dew_point_F": round(dew_point * 9/5 + 32, 2)
            }

            response = json.dumps(data)
        except Exception as e:
            response = json.dumps({"error": "Failed to read sensor", "details": str(e)})
            led_fade_error()  # Indicate an error

        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
            "Access-Control-Allow-Headers: Content-Type\r\n"
            "\r\n"
        )

        client.send(response_headers + response)
        client.close()

# Main loop to check Wi-Fi connection
while True:
    if wlan.isconnected():
        led_slow_blink()  # Indicate connected status
    else:
        led_fast_blink()  # Indicate lost connection
        wlan.connect(SSID, PASSWORD)  # Attempt reconnection

    time.sleep(1)
    start_server()
