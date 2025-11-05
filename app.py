from flask import Flask, render_template, request, jsonify
from tempsensor import read_temp
from mode_database import save_mode_to_db, load_latest_mode
from debug import Debugger
from data_connector.connector_manager import ConnectorManager
from mode_database import init_db

app = Flask(__name__)
init_db()
current_mode = load_latest_mode()  # Modus beim Start laden
debug = Debugger()
connector_manager = ConnectorManager()


@app.route('/')
def index():
    mode = load_latest_mode()  # Immer aktuellen Modus aus DB holen
    return render_template('index.html', mode=mode)

@app.route('/temperature')
def temperature():
    #temp = read_temp()
    value = connector_manager.get("temperature")
    return jsonify({'temperature': value})

@app.route('/set_mode', methods=['POST'])
def set_mode():
    data = request.get_json()
    mode = data.get('mode')
    debug.log(f"Empfangener Modus: {mode}", label="Moduswechsel")
    if mode in ['auto', 'manual']:
        save_mode_to_db(mode)
        mode = load_latest_mode()  # Direkt aus DB laden
        return jsonify({'mode': mode})
    return jsonify({'error': 'Ungültiger Modus'}), 400

@app.route('/set_fan_speed', methods=['POST'])
def set_fan_speed():
    data = request.get_json()
    speed = data.get('speed')
    debug.log(f"Lüftergeschwindigkeit gesetzt: {speed}%", label="Lüftersteuerung")
    # Hier könntest du GPIO/PWM ansteuern
    return jsonify({'status': 'ok', 'speed': speed})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
