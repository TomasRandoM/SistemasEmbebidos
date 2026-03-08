import serial
import time
import ntplib
from flask import Flask, request, jsonify

app = Flask(__name__)

cliente = ntplib.NTPClient()

respuesta = cliente.request('pool.ntp.org')

unix_time = int(respuesta.tx_time)
c_time = time.ctime(respuesta.tx_time)


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

@app.route("/getEEPROM", methods=["GET"])
def getEEPROM():
    ser.write(b"1\n")
    line = ser.readline().decode("utf-8").strip()
    items = line.strip().split(',')
    unique_items = list(dict.fromkeys(items))

    events = []

    for item in unique_items:
        if item:
            valor, pin = item.split('-')
            events.append({
                "timestamp": time.ctime(int(valor)),
                "pin": int(pin)
            })

    return jsonify(events)

@app.route("/deleteEEPROM", methods=["GET"])
def deleteEEPROM():
    ser.write(b"2\n")
    return "OK", 200

@app.route("/updateTime", methods=["GET"])
def updateTime():
    respuesta = cliente.request('pool.ntp.org')
    unix_time = int(respuesta.tx_time)
    unixTimeSend = ("0," + str(unix_time) + "\n")
    ser.write(unixTimeSend.encode("utf-8"))
    
    return jsonify({"time" : time.ctime(int(unix_time))}), 200


if __name__ == "__main__":
    unixTimeSend = ("0," + str(unix_time) + "\n")
    ser.write(unixTimeSend.encode("utf-8"))
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)

    

