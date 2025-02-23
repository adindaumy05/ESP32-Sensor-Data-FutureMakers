import network
import ujson
import urequests
import utime
import machine

# Konfigurasi WiFi
SSID = "GaGratisYaa!!!"
PASSWORD = "malesgamaukasih!"

# Konfigurasi Server Flask
FLASK_URL = "http://192.168.1.100:5000/post_data"

# Konfigurasi MongoDB
MONGO_URI = "mongodb+srv://adindaummy05:<UhWQfObXndHnNV2R>@dinda56.5rvzo.mongodb.net/?retryWrites=true&w=majority&appName=dinda56"
DATABASE_NAME = "sensor_data_SIC6_FutureMakers"
COLLECTION_NAME = "ldr_pir_data"

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBUS-wXHsaMFM0kflZOFhjzVCJhAOXvFNGr"
UBIDOTS_DEVICE_LABEL = "sic-dashboard-future-makers"
UBIDOTS_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/sic-dashboard-future-makers/"

# Inisialisasi sensor
ldr = machine.ADC(machine.Pin(34)) 
ldr.atten(machine.ADC.ATTN_11DB)    
pir = machine.Pin(27, machine.Pin.IN)  

# Koneksi ke WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        utime.sleep(1)
    print("Terhubung ke WiFi:", wlan.ifconfig())

connect_wifi()

# Kirim Data ke Flask dan MongoDB
def send_data():
    while True:
        ldr_value = ldr.read()
        pir_value = pir.value()
        data = {"ldr": ldr_value, "pir": pir_value}

        try:
            response = urequests.post(FLASK_URL, json=data)
            print("Data Terkirim:", response.json())
        except Exception as e:
            print("Error:", e)

        utime.sleep(5)  # Kirim setiap 5 detik

send_data()

# Koneksi ke MongoDB
def connect_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db[COLLECTION_NAME]

# Kirim data ke Ubidots
def send_to_ubidots(ldr_value, pir_value):
    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
    data = {"ldr": ldr_value, "pir": pir_value}
    try:
        response = urequests.post(UBIDOTS_URL, json=data, headers=headers)
        print("Data sent to Ubidots:", response.text)
    except Exception as e:
        print("Ubidots Error:", e)

# Loop utama
def main():
    connect_wifi()
    while True:
        ldr_value = ldr.read()
        pir_value = pir.value()
        
        print(f"LDR: {ldr_value}, PIR: {pir_value}")

        send_to_mongo(ldr_value, pir_value)
        send_to_ubidots(ldr_value, pir_value)

        utime.sleep(5)  # Kirim data setiap 5 detik

# Jalankan program utama
main()
