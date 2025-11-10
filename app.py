from flask import Flask, render_template, request, jsonify
from debug import Debugger
from data_connector.connector_manager import ConnectorManager

app = Flask(__name__)
debug = Debugger()
connector_manager = ConnectorManager()


@app.route('/')
def index():
    mode = connector_manager.get("mode")  # Immer aktuellen Modus aus DB holen
    return render_template('index.html', mode=mode, active_page='home')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html', active_page='analysis')

@app.route('/config')
def config():
    return render_template('config.html', active_page='config')

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
        connector_manager.set("mode", mode)         # Modus speichern über Manager
        current_mode = connector_manager.get("mode")  # Modus lesen über Manager
        return jsonify({'mode': current_mode})
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
