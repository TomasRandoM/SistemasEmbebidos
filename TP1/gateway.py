import serial
import time
from flask import Flask, request, jsonify


app = Flask(__name__)

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

@app.route("/changeLedValue", methods=["POST"])
def changeLedValue():
    pin = request.form.get("pin")
    value = request.form.get("valor")
    if (pin == "9" or pin == "10" or pin == "11"):
        value = int(value) * 255 / 100
    digitalString = "0," + str(pin) + "," + str(value) + "\n"
    ser.write((digitalString).encode("utf-8"))
    return "OK", 200

@app.route("/getLedsValue", methods=["GET"])
def getLedValue():
    ser.write(b"1\n")
    line = ser.readline().decode("utf-8").strip()
    print("line: ", line)
    led9, led10, led11, led13, ldr = line.split(",")
    return jsonify({
        "brilloLed9": led9,
        "brilloLed10": led10,
        "brilloLed11": led11,
        "led13": led13,
        "valorLDR": ldr
    })
    

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)