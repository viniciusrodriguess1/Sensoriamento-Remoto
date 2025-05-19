from fastapi import FastAPI
import serial
import threading
import time

app = FastAPI()

serial_port = '/dev/tty.usbserial-110'
baud_rate = 9600
data_from_arduino = ""
ser = None
serial_lock = threading.Lock()

def read_serial_data():
    global data_from_arduino, ser
    while True:
        if ser and ser.is_open:
            try:
                new_data = ser.readline().decode('utf-8').strip()
                with serial_lock:
                    data_from_arduino = new_data
                print(f"Data received from Arduino: {data_from_arduino}")
            except serial.SerialException as e:
                print(f"Serial port error: {e}")
                time.sleep(2)
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")
        else:
            time.sleep(1)

@app.on_event("startup")
def startup_event():
    global ser
    try:
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Serial port {serial_port} opened successfully.")
        serial_thread = threading.Thread(target=read_serial_data, daemon=True)
        serial_thread.start()
    except serial.SerialException as e:
        print(f"Error opening serial port {serial_port}: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    if ser and ser.is_open:
        ser.close()
        print(f"Serial port {serial_port} closed.")

@app.get("/arduino_data")
async def get_arduino_data():
    with serial_lock:
        return {"data": data_from_arduino}
    
def read_serial_data():
    global data_from_arduino, ser
    while True:
        if ser and ser.is_open:
            try:
                new_data = ser.readline().decode('utf-8').strip()
                print(f"Raw data from Arduino: '{new_data}'") # Adicione este log
                with serial_lock:
                    data_from_arduino = new_data
                print(f"Data stored: {data_from_arduino}")
            except serial.SerialException as e:
                print(f"Serial port error: {e}")
                time.sleep(2)
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")
        else:
            time.sleep(1)
