CTF: Operation “Silent Signal” - Student Handout

Goal: Find 3 flags in a small web lab and document your process professionally.
Target & Setup

Target: ctf.geekink.local (HTTP :8000) and debug service on :8080.

Instructor will provide <SERVER_IP>. Map hosts with:
sudo sh -c 'echo "<SERVER_IP> ctf.geekink.local dev.ctf.geekink.local" >> /etc/hosts'

What to do (high level)
1) Recon: use ping, dig/nslookup, nmap (light scans) to discover services.
2) Explore site and robots.txt (request as dev subdomain).
3) Inspect headers on port 8080 (look for leaked headers).
4) Use Burp Repeater / curl to experiment with login form (basic SQLi).
5) Record commands, screenshots, raw outputs; create CherryTree notes.
Minimal Hints

• Flag #1: Check robots.txt for dev subdomain (use Host header or dev.ctf... mapping).

• Flag #2: Response header on debug service (:8080) contains a flag.

• Flag #3: Send an auth payload with a SQL tautology (e.g., ' OR '1'='1) to /auth.
Deliverables & Grading
Deliverables:

- example_ctf_<name>_notes.ctb (CherryTree notes with screenshots & timestamps)
  
- flags.txt (3 flags + one-line how found each)
  
- summary.md (1-page report: exec summary, findings, remediation)
- 
Grading: Flags 50% | Notes 30% | Report 20%
Rules & Quick Commands
Rules: Passive + light active recon only. No destructive tests. Document and report accidental out-of-scope actions.

Quick commands:
ping -c4 ctf.geekink.local
dig ctf.geekink.local ANY +noall +answer

curl -v -H "Host: dev.ctf.geekink.local" http://<SERVER_IP>:8000/robots.txt

curl -I http://<SERVER_IP>:8080/

curl -v -X POST -d "username=admin&password=' OR '1'='1" http://<SERVER_IP>:8000/auth
