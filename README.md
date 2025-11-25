## CTF Web Environment - Operation Silent Signal
--------------------------------------------
Files:
  - app.py          : Flask app that runs two services (8000 and 8080)
  - templates/      : HTML templates (index, login, welcome)
  - requirements.txt: Python dependencies
  - run_ctf.sh      : helper script to run the app
  - README.txt      : this file

How to run (on your Kali VM):
  1. Ensure Python 3 and pip are installed.
     sudo apt update && sudo apt install -y python3 python3-pip
  2. Install dependencies:
     pip3 install -r requirements.txt
  3. Run the app (no root needed):
     ./run_ctf.sh
  4. Access the services from the same machine or other VMs by mapping hosts:
     - Edit /etc/hosts on your VM or host and add:
         127.0.0.1   ctf.geekink.local dev.ctf.geekink.local
       (replace 127.0.0.1 with your server's IP if running on another machine)
  5. Open browser and visit:
     http://ctf.geekink.local:8000
     http://ctf.geekink.local:8080  (debug service; check response headers)

Flags:
  - FLAG{DNS_DISCOVERY_WINNER}     (appears in robots.txt when Host header indicates dev.ctf...)
  - FLAG{NMAP_DISCOVERY_SUCCESS}   (X-Debug-Info header from service on port 8080)
  - FLAG{BASIC_SQLI_SUCCESS}       (returned on successful SQLi-like auth payload)

Notes for instructors:
  - The robots.txt route checks the Host header. Instructors can demonstrate mapping dev.ctf... in /etc/hosts so students can request dev.ctf.geekink.local:8000/robots.txt
  - The debug service returns the header on any request. Show students how to use curl -v or Burp to see response headers.
  - The SQLi is simulated: if password contains typical tautology payloads, the server responds with the flag.
