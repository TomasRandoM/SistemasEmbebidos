import serial
import pickle
import ntplib
import time
from flask import Flask
from flask_cors import CORS
import threading

cliente = ntplib.NTPClient()

list = []

app = Flask(__name__)
CORS(app)

ser = 0
while True:
    try:
        ser = serial.Serial(port='COM5', 
                    baudrate=9600, 
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE, 
                    stopbits=serial.STOPBITS_ONE, 
                    timeout=1,
                    xonxoff=False, 
                    rtscts=False, 
                    dsrdtr=False, 
                    inter_byte_timeout=None,
                    exclusive=None)
        break
    except:
        print("ERROR conectando al arduino")
        time.sleep(1)



def readSerial():
    global channel
    global list
    global ser
    try:
        with open("lecturas.pkl", "rb") as f:
            list = pickle.load(f)
    except:
        list = []
    while True:
        try:
            ser.write(b"0\n")
            value = ser.readline().decode("utf-8").strip()

            unix_time = int(time.time())
            
            data = {"timestamp": unix_time, "ldr_value": value}

            list.append(data)

            with open("lecturas.pkl", "wb") as f:
                pickle.dump(list, f)
        except serial.SerialException:
            ser = serial.Serial(port='COM5', 
                    baudrate=9600, 
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE, 
                    stopbits=serial.STOPBITS_ONE, 
                    timeout=1,
                    xonxoff=False, 
                    rtscts=False, 
                    dsrdtr=False, 
                    inter_byte_timeout=None,
                    exclusive=None)
            print("ERROR conectando al arduino")
        time.sleep(5)
        
        
if __name__ == "__main__":
    thread = threading.Thread(target=readSerial)
    thread.daemon = True
    thread.start()
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)
