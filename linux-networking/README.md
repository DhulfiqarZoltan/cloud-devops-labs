# Linux Networking Lab: Fix Connection Refused
Author: Dr. Alwahab Dhulfiqar Zoltan

## What you will learn
Run the same small Python app as the permissions lesson; diagnose a wrong-port error using process checks, TCP listeners, HTTP responses and logs. Compare loopback with an optional wildcard bind, then practise on port 8080.

## Prerequisites and setup
Ubuntu 24.04 VM or Ubuntu on WSL2; Bash, Python 3, curl and iproute2 (ss). On macOS use an Ubuntu VM. No cloud account or paid resources. Run ALL commands in the same Linux environment and keep the terminal open. The recording uses a fresh, externally isolated Ubuntu container; Docker is not required for students.

If needed, install tools in Ubuntu:
```bash
sudo apt-get update
sudo apt-get install -y python3 curl iproute2 procps unzip
```
Extract `linux-networking-lab.zip` into your Linux home directory. The result should be `~/linux-networking-lab/app.py`. Move the extracted directory there if your download tool put it elsewhere. The app uses only Python's standard library. It is a teaching server, not production software.

## Follow along: one command at a time

### Open the supplied folder
```bash
cd ~/linux-networking-lab
```
Extract the ZIP into your Linux home directory first.

### Inspect the lab files
```bash
ls
```
Expected: app.py, README.md, SOLUTION.md and LICENSE

### Check Python
```bash
python3 --version
```
Any supported Python 3 version is suitable for this small app.

### Check the HTTP client
```bash
curl --version | head -n 1
```
curl sends the request; it does not start the server.

### Check the listening ports
```bash
ss -ltn 'sport = :8000'
```
An empty result below the header means no TCP listener matched.
If a process already uses 8000, inspect it and choose a disposable clean environment; do not terminate unrelated processes.

### Start the app in the background
```bash
python3 app.py >app.log 2>&1 &
```
The ampersand returns control to your shell.

### Save this run’s process number
```bash
app_pid=$!
```
Run immediately after starting the background app.

### Verify the process identity
```bash
ps -p "$app_pid" -o pid,user,args
```
Confirm this PID belongs to python3 app.py.

### Create the wrong-port error
```bash
curl --noproxy "*" --max-time 3 http://127.0.0.1:8001/health
```
Intentional failure: curl exit 7, connection refused.
Expected curl exit code: 7. Run this intentionally failing command interactively; do not paste the full lesson into a script with `set -e`.

### Find the actual listener
```bash
ss -ltnp 'sport = :8000'
```
Look for 127.0.0.1:8000 and python3.

### Send the corrected request
```bash
curl --noproxy "*" --fail --show-error http://127.0.0.1:8000/health
```
Expected response body: OK

### Inspect the HTTP response
```bash
curl --noproxy "*" -i http://127.0.0.1:8000/health
```
The status line and body answer different questions.

### Read the application log
```bash
tail -n 5 app.log
```
Successful requests appear here; a refused connection may not.

### Stop only this lab process
```bash
kill -TERM "$app_pid"; wait "$app_pid"; true
```
We already verified this PID with ps.

### Verify the listener is gone
```bash
ss -ltn 'sport = :8000'
```
No matching listener remains.

### Compare a wildcard bind
```bash
BIND=0.0.0.0 python3 app.py >app.log 2>&1 &
```
Disposable lab only: this accepts connections on available IPv4 interfaces.
Optional comparison: skip the wildcard bind on a shared/networked machine. It accepts traffic on all available IPv4 interfaces; it does not open firewalls or provide authentication. Stop it promptly after the check.

### Save the new process number
```bash
app_pid=$!
```
Every new run has a new process number.

### Observe the wildcard listener
```bash
ss -ltnp 'sport = :8000'
```
0.0.0.0 is a listening address, not the client URL to copy.

### Test using a real destination
```bash
curl --noproxy "*" --fail http://127.0.0.1:8000/health
```
Wildcard listener, loopback client request: OK.

### Confirm the process before cleanup
```bash
ps -p "$app_pid" -o pid,user,args
```
Check again before stopping this run.

### Stop the comparison server
```bash
kill -TERM "$app_pid"; wait "$app_pid"; true
```
Keep your lab environment tidy.

### Final socket check
```bash
ss -ltn 'sport = :8000'
```
Expected: no listener on port 8000.

## Understanding the evidence
- `127.0.0.1` is loopback inside the Linux environment running the command. A VM/container has its own network context.
- `8000` is the server's port; `8001` is deliberately wrong in the main example.
- `ss -ltnp` shows TCP listeners numerically with available process information. Seeing other users' process details may require privileges; our app belongs to our own user.
- `0.0.0.0` is a wildcard server bind, not the client destination to use. Request `127.0.0.1` locally; remote access also depends on actual addresses, routing and firewall policy.
- A refused connection is different from an HTTP 404. Refusal alone does not identify every possible network cause; here the clean lab and socket evidence establish the wrong-port cause.
- `app_pid=$!` must immediately follow each background launch. Check `ps` before terminating it. Keep the same shell open.
- `curl --noproxy "*"` bypasses proxy configuration for these direct local lab requests.

## Exercise — try before reading SOLUTION.md
Start the app on port 8080 with its default loopback bind. Save and verify its PID. Find the listener, request `/health`, show that port 8000 no longer works, then stop only your app. Confirm both ports have no remaining lab listener. Explain the address/port mismatch in one sentence.

## Troubleshooting
Missing tools: install the prerequisites. Missing folder: check extraction. Process exits immediately: inspect `cat app.log`; `Address already in use` means check existing listeners. No process details in ss: inspect your own user/process and permissions. Wrong output from curl: verify no unrelated service owns that port. If a command is interrupted, inspect the real current state before retrying.

## Official documentation
- ss: https://man7.org/linux/man-pages/man8/ss.8.html
- curl: https://curl.se/docs/manpage.html
- Python HTTPServer: https://docs.python.org/3.12/library/http.server.html
- Bash job control: https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html
- Ubuntu networking: https://ubuntu.com/server/docs/configuring-networks/

Copyright Dr. Alwahab Dhulfiqar Zoltan. See LICENSE.
