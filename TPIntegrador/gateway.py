import serial
import time
from flask import Flask, jsonify, render_template
import requests
import threading
from flask_socketio import SocketIO
from flask_cors import CORS

apiVideoUrl = "http://127.0.0.1:3001/video/"
channel = 1

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
#Inicializamos el serial
ser = serial.Serial(port='COM3', 
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
    return render_template("index.html")

def test():
    try:
        value = 2
        response = requests.get(apiVideoUrl + str(value))
        if (response.status_code == 200):
            socketio.emit("changeChannel", response.json())
        else:
            socketio.emit("changeChannel", {"error": "API Didn't Respond"})
    except requests.exceptions.RequestException as e:
        return
    
@app.route("/start", methods=["GET"])
def start():
    ser.write(b"0\n")
    global channel
    time.sleep(1)
    try:
        response = requests.get(apiVideoUrl + str(channel))
        if (response.status_code == 200):
            ser.write(("-3," + str(response.json()["totalVideos"]) + "\n").encode("utf-8"))
            return response.json(), 200
        else:
            return ({"error": "API Didn't Respond"}), 503
    except requests.exceptions.RequestException as e:
        return ({"error": "API Didn't Respond"}), 503

def readSerial():
    global channel
    while True:
        value = ser.readline().decode("utf-8").strip()
        try:
            value = int(value)
            if (value == -2):
                channel -= 1
            elif (value == -1):
                channel += 1
            else:
                channel = value
            if (value == -2 or value == -1):
                try:
                    response = requests.get(apiVideoUrl + str(channel))
                    if (response.status_code == 200):
                        channel = int(response.json()["id"])
                        socketio.emit("changeChannel", response.json())
                    else:
                        socketio.emit("changeChannel", {"error": "API Didn't Respond"})
                except requests.exceptions.RequestException as e:
                    continue
        except ValueError:
            continue

@app.route("/changeChannel/<int:id>", methods=["GET"])
def changeChannel(id):
    global channel
    id = str(id)
    try:
        response = requests.get(apiVideoUrl + id)
        ser.write((str(response.json()["id"]) + "\n").encode("utf-8"))
        if (response.status_code == 200):
            channel = int(response.json()["id"])
            socketio.emit("changeChannel", response.json())
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

    

