from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from utils.configManager import ConfigManager
from debug import Debugger
from data_connector.connector_manager import ConnectorManager

app = Flask(__name__)
debug = Debugger()
connector_manager = ConnectorManager()
config_manager = ConfigManager("config.json")

@app.route('/')
def index():
    mode_data = connector_manager.get("mode")  # liefert dict {"mode":..., "fan_speed":...}
    fan_type = config_manager.get_fan_type()
    return render_template(
        'index.html',
        mode=mode_data["mode"],
        fan_speed=mode_data["fan_speed"],
        fan_type=fan_type,
        active_page='home'
    )

@app.route('/analysis')
def analysis():
    return render_template('analysis.html', active_page='analysis')

@app.route('/config', methods=["GET", "POST"])
def config():
    levels = config_manager.get_threshold_levels()

    if request.method == "POST":
        thresholds = {}
        for level in levels:
            key = f"threshold_{level}"
            value = request.form.get(key)
            if value:
                thresholds[level] = float(value)
        connector_manager.set("threshold", thresholds)

        mode = request.form.get("mode_toggle") == "on"
        interval_days = int(request.form.get("day_select", 1))
        connector_manager.set("analysis", {"mode": mode, "interval_days": interval_days})

        return redirect(url_for("config"))

    current_thresholds = connector_manager.get("threshold") or {}
    analysis = connector_manager.get("analysis") or {"mode": False, "interval_days": 1}

    return render_template("config.html", active_page="config", thresholds=current_thresholds, analysis=analysis,
        levels=levels)

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
        mode_data = connector_manager.get("mode")  # dict mit {"mode":..., "fan_speed":...}

        # Wenn Automatikmodus aktiviert wurde → Lüftergeschwindigkeit auf 0 setzen
        if mode_data["mode"] == "auto":
            connector_manager.connectors["mode"].write_fan_speed(0)
            debug.log("Fan speed auf 0 gesetzt wegen Automatikmodus", label="Moduswechsel")

        return jsonify(mode_data)
    return jsonify({'error': 'Ungültiger Modus'}), 400

@app.route('/set_fan_speed', methods=['POST'])
def set_fan_speed():
    data = request.get_json()
    speed = data.get('speed', 0)
    debug.log(f"Lüftergeschwindigkeit gesetzt: {speed}%", label="Lüftersteuerung")
    connector_manager.connectors["mode"].write_fan_speed(speed)

    return jsonify({'status': 'ok', 'speed': speed})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
