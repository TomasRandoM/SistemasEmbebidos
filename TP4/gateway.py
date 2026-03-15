import serial
import time
from flask import Flask, jsonify, render_template
import threading
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
#Inicializamos el serial
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


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/erase", methods=["GET"])
def erase():
    try:
        ser.write(b"-3\n")
    except:
        print("ERROR conectando al arduino")
        time.sleep(2)
    return "OK", 200

@app.route("/start", methods=["GET"])
def start():
    ser.write(b"-4\n")
    return "OK", 200

def readSerial():
    global ser
    while True:
        try:
            value = ser.readline().decode("utf-8").strip()
            try:
                value = int(value)
                if (value == -2):
                    socketio.emit("alarm", {"state" : False})
                elif (value == -1):
                    socketio.emit("alarm", {"state" : True})
                elif (value == -5):
                    socketio.emit("person", {"state" : True})
                elif (value == -6):
                    socketio.emit("person", {"state" : False})
                else:
                    socketio.emit("people", {"quantity" : value})
            except ValueError:
                continue
        except serial.SerialException:
            try:
                print("ERROR conectando al arduino")
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
            except:
                print("ERROR conectando al arduino")
                time.sleep(2)


if __name__ == "__main__":
    thread = threading.Thread(target=readSerial)
    thread.daemon = True
    thread.start()
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)

    

