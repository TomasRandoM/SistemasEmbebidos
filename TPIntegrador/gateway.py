import serial
import time
from flask import Flask, jsonify
import requests
import threading
from flask_socketio import SocketIO

apiVideoUrl = "http://127.0.0.1:3001/video/"

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

#Inicializamos el serial
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
time.sleep(2)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/start", methods=["GET"])
def start():
    ser.write(b"0\n")
    line = ser.readline().decode("utf-8").strip()
    channel = int(line)
    try:
        response = requests.get(apiVideoUrl + str(channel))
        if (response.status_code == 200):
            return response.json(), 200
        else:
            return ({"error": "API Didn't Respond"}), 503
    except requests.exceptions.RequestException as e:
        return ({"error": "API Didn't Respond"}), 503

def readSerial():
    global alarm
    global ldrValue
    global readActivated
    while True:
        value = ser.readline().decode("utf-8").strip()
        try:
            value = int(value)
            try:
                response = requests.get(apiVideoUrl + str(value))
                if (response.status_code == 200):
                    socketio.emit("changeChannel", response.json())
                else:
                    socketio.emit("changeChannel", {"error": "API Didn't Respond"})
            except requests.exceptions.RequestException as e:
                continue
        except ValueError:
            continue

@app.route("/changeChannel/<int:id>", methods=["GET"])
def changeChannel(id):
    id = str(id)
    ser.write((id + "\n").encode())
    try:
        response = requests.get(apiVideoUrl + id)
        if (response.status_code == 200):
            return (response.json()), 200
        else:
            return jsonify({"error": "API Didn't Respond"}), 503
    except requests.exceptions.RequestException as e:
        return ({"error": "API Didn't Respond"}), 503
    

if __name__ == "__main__":
    thread = threading.Thread(target=readSerial)
    thread.daemon = True
    thread.start()
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)

    

