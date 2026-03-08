from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)


alarm = False
ldrValue = 0
readActivated = True

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

@app.route("/valor", methods=["GET"])
def getValue():
    return jsonify({
        "alarm": alarm,
        "ldrValue": ldrValue,
        "readActivated": readActivated
    }), 200

@app.route("/start", methods=["POST"])
def startReading():
    ser.write("-2\n".encode("utf-8"))

@app.route("/stop", methods=["POST"])
def startReading():
    ser.write("-3\n".encode("utf-8"))

def readSerial():
    global alarm
    global ldrValue
    global readActivated
    while True:
        value = int(ser.readline().decode("utf-8").strip())
        if (value == -1):
            alarm = True
        elif (value == -2):
            readActivated = True
        elif (value == -3):
            readActivated = False
        elif (value == -4):
            alarm = False
        else:
            ldrValue = value

if __name__ == "__main__":
    thread = threading.Thread(target=readSerial)
    thread.daemon = True
    thread.start()
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)

    

