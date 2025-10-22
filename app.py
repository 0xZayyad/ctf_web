#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, url_for, make_response, jsonify
import threading, logging

# Main app (port 8000)
app = Flask(__name__, template_folder="templates")

# Simple in-memory "users" (for realism, but not actually used)
USERS = {"admin":"s3cr3t"}

# Flag constants
FLAG1 = "FLAG{DNS_DISCOVERY_WINNER}"
FLAG2 = "FLAG{NMAP_DISCOVERY_SUCCESS}"
FLAG3 = "FLAG{BASIC_SQLI_SUCCESS}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    # Accept either form or JSON so students can experiment with both
    if request.is_json:
        data = request.get_json(force=True)
        username = data.get("username","")
        password = data.get("password","")
    else:
        username = request.form.get("username","")
        password = request.form.get("password","")
    # naive SQLi simulation: if payload contains SQL tautology, return flag
    if "\" OR \"" in password or "' OR '" in password or "OR 1=1" in password.upper():
        resp = make_response(render_template("welcome.html", user="admin", flag=FLAG3))
        return resp
    # normal auth failure
    return make_response("Authentication failed", 401)

@app.route("/robots.txt")
def robots():
    # If the Host header indicates the dev subdomain, return the hidden flag path
    host = request.headers.get("Host","")
    if host.startswith("dev.") or host.startswith("dev"):
        content = "User-agent: *\\nDisallow: /hidden_flag/\\n# " + FLAG1 + "\\n"
        r = make_response(content, 200)
        r.mimetype = "text/plain"
        return r
    # default robots
    content = "User-agent: *\\nDisallow:\\n"
    r = make_response(content, 200)
    r.mimetype = "text/plain"
    return r

@app.route("/hidden_flag/")
def hidden_flag():
    # This should only be visible if robots pointed to it; keep it simple
    return "<pre>{}</pre>".format(FLAG1)

# Secondary debug service (port 8080) will be a small Flask app that sets a debug header
debug_app = Flask("debug_app")

@debug_app.route("/", defaults={"path":""})
@debug_app.route("/<path:path>")
def debug_index(path):
    resp = make_response("Inkverse Labs Test Service - debug endpoint\\n")
    resp.headers["X-Debug-Info"] = FLAG2
    return resp

def run_main():
    # Disable Flask's logging to keep output clean for students
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=8000, debug=False)

def run_debug():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    debug_app.run(host="0.0.0.0", port=8081, debug=False)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_main, daemon=True)
    t2 = threading.Thread(target=run_debug, daemon=True)
    t1.start()
    t2.start()
    print("CTF web environment running:")
    print(" - Main app: http://<host>:8000  (use Host header ctf.geekink.local or map /etc/hosts)")
    print(" - Debug service: http://<host>:8080  (X-Debug-Info header contains a flag)")
    try:
        while True:
            t1.join(1)
            t2.join(1)
    except KeyboardInterrupt:
        print("\nStopping CTF servers...")
