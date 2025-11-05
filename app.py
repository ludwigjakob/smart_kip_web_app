from flask import Flask, render_template, request, jsonify
from tempsensor import read_temp
from statemachine import load_mode, save_mode
from debug import Debugger
from data_connector.connector_manager import ConnectorManager

app = Flask(__name__)
current_mode = load_mode()  # Modus beim Start laden
debug = Debugger()
connector_manager = ConnectorManager()

@app.route('/')
def index():
    return render_template('index.html', mode=current_mode)

@app.route('/temperature')
def temperature():
    #temp = read_temp()
    value = connector_manager.get("temperature")
    return jsonify({'temperature': value})

@app.route('/set_mode', methods=['POST'])
def set_mode():
    global current_mode
    data = request.get_json()
    mode = data.get('mode')
    debug.log(f"Empfangener Modus: {mode}", label="Moduswechsel")
    if mode in ['auto', 'manual']:
        current_mode = mode
        save_mode(current_mode)  # Modus speichern
    return jsonify({'mode': current_mode})

@app.route('/set_fan_speed', methods=['POST'])
def set_fan_speed():
    data = request.get_json()
    speed = data.get('speed')
    debug.log(f"Lüftergeschwindigkeit gesetzt: {speed}%", label="Lüftersteuerung")
    # Hier könntest du GPIO/PWM ansteuern
    return jsonify({'status': 'ok', 'speed': speed})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
