import network
import urequests
import utime
import machine

# --- Konfigurasi WiFi ---
    WIFI_SSID = "GaGratisYaa!!!"
    WIFI_PASS = "malesgamaukasih!"

# --- Konfigurasi Ubidots ---
    UBIDOTS_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/sic-dashboard-future-makers/"
    UBIDOTS_TOKEN = "BBUS-wXHsaMFM0kflZOFhjzVCJhAOXvFNGr" 

# --- Konfigurasi Firebase ---
    FIREBASE_URL = "https://sic6-futuremakers-ass2-default-rtdb.asia-southeast1.firebasedatabase.app/sensor_data.json"


# --- Inisialisasi Sensor ---
    ldr = machine.ADC(machine.Pin(36))  # LDR di GPIO36
    pir = machine.Pin(27, machine.Pin.IN)  # PIR di GPIO27

# --- Fungsi Koneksi ke WiFi ---
    def connect_wifi():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
        print("Terhubung ke WiFi:", wlan.ifconfig())

# --- Fungsi Kirim Data ke Ubidots
    def send_to_ubidots(ldr_value, pir_value):
        payload_ubidots = {
            "ldr": ldr_value,
            "pir": pir_value
        }
        headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
        try:
            response = urequests.post(UBIDOTS_URL, json=payload_ubidots, headers=headers)
            print("Ubidots:", response.json())  # Debugging response
        except Exception as e:
            print("Ubidots Error:", e)

# --- Fungsi Kirim Data ke Firebase ---
    data = {
        "ldr": ldr_value,
        "pir": pir_value,
        "timestamp": utime.time()
    }
    try:
        response = urequests.put(FIREBASE_URL, json=data)  # Gunakan put() agar data diperbarui
        print("Firebase:", response.text)
    except Exception as e:
        print("Firebase Error:", e)

# --- Main Loop: Kirim Data Setiap 5 Detik ---
    connect_wifi()
    while True:
        ldr_value = ldr.read()  # Baca LDR
        pir_value = pir.value()  # Baca PIR
        
        print(f"LDR: {ldr_value}, PIR: {pir_value}")
        
        send_to_ubidots(ldr_value, pir_value)
        send_to_firebase(ldr_value, pir_value)
        
        utime.sleep(5)  # Kirim setiap 5 detik
