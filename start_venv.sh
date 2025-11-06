#!/bin/bash

# Virtuelle Umgebung aktivieren
source venv/bin/activate

# Umgebungsvariablen aus .env laden
set -a
source .env
set +a

# Flask starten
flask run
