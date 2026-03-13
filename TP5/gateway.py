import serial
import pickle
import time
from flask import Flask, send_file, render_template
from flask_cors import CORS
import threading
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import io

lista = []

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

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
    global lista
    global ser
    try:
        with open("lecturas.pkl", "rb") as f:
            lista = pickle.load(f)
    except:
        lista = []
    while True:
        try:
            ser.write(b"0\n")
            value = ser.readline().decode("utf-8").strip()
            try:
                value = int(value)
                print(value)
            except ValueError:
                continue
            unix_time = int(time.time())
            #Aca se redondea al más bajo por problemas de compatibilidad al graficar si el servidor se detenía
            unix_time = unix_time - (unix_time % 5)
            data = {"timestamp": unix_time, "ldr_value": value}

            lista.append(data)

            with open("lecturas.pkl", "wb") as f:
                pickle.dump(lista, f)
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
        time.sleep(5)

@app.route("/plot", methods=["GET"])
def makeImage():
    df = pd.DataFrame(lista)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('America/Argentina/Buenos_Aires')
    df['ldr_value'] = df['ldr_value'].astype(float)
    df.set_index('datetime', inplace=True)

    #Se setea un índice nuevo que sea cada 5s
    start = df.index.min()
    end = df.index.max()
    full_index = pd.date_range(start=start, end=end, freq='5s')  
    df = df.reindex(full_index)

    fig = plt.figure(figsize=(10,5))
    plt.plot(df.index, df['ldr_value'], marker='o')
    plt.xlabel('Tiempo')
    plt.ylabel('Valor LDR')
    plt.title('Lecturas de LDR')
    plt.grid(True)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')
if __name__ == "__main__":
    thread = threading.Thread(target=readSerial)
    thread.daemon = True
    thread.start()
    matplotlib.use('Agg')
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)
