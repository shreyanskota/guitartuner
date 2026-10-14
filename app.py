"""
Guitar Tuner Web Application
Cloud Computing & DevOps (CCA 2) Project
A lightweight Flask web application serving an interactive guitar tuner
with real-time Web Audio API reference pitch generation and health endpoints for Kubernetes.
"""

from flask import Flask, render_template, jsonify
import math

app = Flask(__name__)

# Application Version (Update this for demonstrating CI/CD Stage 9 redeployment)
APP_VERSION = "1.0.0"
APP_THEME = "classic-cyan"

# Standard 6-String Guitar Tuning Reference Frequencies (in Hertz)
# String numbering: 1 is highest pitch (High E), 6 is lowest pitch (Low E)
GUITAR_STRINGS = [
    {"number": 6, "note": "E", "octave": 2, "name": "6th (Low E)", "frequency": 82.41,  "gauge": "0.046"},
    {"number": 5, "note": "A", "octave": 2, "name": "5th (A)",     "frequency": 110.00, "gauge": "0.036"},
    {"number": 4, "note": "D", "octave": 3, "name": "4th (D)",     "frequency": 146.83, "gauge": "0.026"},
    {"number": 3, "note": "G", "octave": 3, "name": "3rd (G)",     "frequency": 196.00, "gauge": "0.017"},
    {"number": 2, "note": "B", "octave": 3, "name": "2nd (B)",     "frequency": 246.94, "gauge": "0.013"},
    {"number": 1, "note": "E", "octave": 4, "name": "1st (High E)","frequency": 329.63, "gauge": "0.010"}
]


def get_string_frequency(string_number):
    """Retrieve the standard frequency for a given string number (1-6)."""
    for s in GUITAR_STRINGS:
        if s["number"] == int(string_number):
            return s["frequency"]
    return None


def calculate_cents_offset(frequency, target_frequency):
    """
    Calculate the tuning deviation in cents between two frequencies.
    Formula: 1200 * log2(frequency / target_frequency)
    """
    if frequency <= 0 or target_frequency <= 0:
        return 0.0
    cents = 1200.0 * math.log2(frequency / target_frequency)
    return round(cents, 2)


def get_app_info():
    """Return dictionary with application release information."""
    return {
        "appName": "Guitar Tuner",
        "version": APP_VERSION,
        "theme": APP_THEME,
        "tuning": "Standard (EADGBE)",
        "totalStrings": len(GUITAR_STRINGS)
    }


@app.route("/")
def index():
    """Main application homepage."""
    return render_template(
        "index.html",
        strings=GUITAR_STRINGS,
        version=APP_VERSION,
        theme=APP_THEME
    )


@app.route("/api/health")
def health_check():
    """
    Kubernetes liveness and readiness probe endpoint.
    Also used by Jenkins pipeline verification stage.
    """
    return jsonify({
        "status": "healthy",
        "service": "guitar-tuner",
        "version": APP_VERSION
    }), 200


@app.route("/api/strings")
def get_strings():
    """API endpoint providing the list of standard tuning strings and frequencies."""
    return jsonify({
        "tuning": "Standard (EADGBE)",
        "strings": GUITAR_STRINGS
    }), 200


@app.route("/api/version")
def version_endpoint():
    """API endpoint exposing application version info."""
    return jsonify(get_app_info()), 200


if __name__ == "__main__":
    # Local development server running on port 3000
    app.run(host="0.0.0.0", port=3000, debug=True)
