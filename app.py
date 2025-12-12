from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from common.utils.configManager import ConfigManager
from common.utils.debug import Debugger
from common.data_connector.connector_manager import ConnectorManager
import requests

app = Flask(__name__)
debug = Debugger()
connector_manager = ConnectorManager()
config_manager = ConfigManager("config.json")
ANALYSIS_URL = "http://localhost:6000"


@app.route('/')
def index():
    mode_data = connector_manager.get("mode")  # liefert dict {"mode":..., "fan_speed":...}
    fan_type = config_manager.get_fan_type()
    sockets = config_manager.get_sockets()
    socket_data = connector_manager.get("socket") if sockets else None


    return render_template(
        'index.html',
        mode=mode_data["mode"],
        fan_speed=mode_data["fan_speed"],
        fan_type=fan_type,
        socket_state=socket_data["state"] if socket_data else None,
        sockets=sockets,
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

@app.route("/sockets")
def get_sockets():
    sockets = config_manager.get_sockets()
    return jsonify(sockets)


@app.route("/socket_status")
def socket_status():
    """Liefert aktuellen Zustand der Socket aus DB."""
    socket_data = connector_manager.get("socket")
    return jsonify(socket_data)

@app.route("/toggle_socket", methods=["POST"])
def toggle_socket():
    """Schreibt neuen Zustand in DB."""
    data = request.get_json()
    state = data.get("state")  # "on" oder "off"
    debug.log(f"Socket gesetzt: {state}", label="Socketsteuerung")

    connector_manager.set("socket", state)
    socket_data = connector_manager.get("socket")
    return jsonify(socket_data)

@app.route('/run_analysis', methods=["POST"])
def run_analysis():
    try:
        # POST an die Analyse-App schicken
        r = requests.post(f"{ANALYSIS_URL}/run")
        if r.status_code == 200:
            debug.log(f"Analysis successfully started", label="analysis")
        else:
            debug.log(f"Fehler beim Starten: {r.text}", label="analysis")
    except Exception as e:
        debug.log(f"Fehler beim Verbinden zur Analyse-App: {e}", label="analysis")
    return redirect(url_for('analysis'))


@app.route('/status_analysis')
def status_analysis():
    try:
        r = requests.get(f"{ANALYSIS_URL}/status")
        return r.json()
    except Exception as e:
        debug.log(f"Fehler beim Abrufen des Status: {e}", label="analysis")
        return {"last_run": "Fehler"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
