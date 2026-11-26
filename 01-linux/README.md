# Linux Permissions Lab — follow-along guide

**Author:** Dr. Alwahab Dhulfiqar Zoltan

Companion to the animated “Permission denied” Short. You will create a real file permission failure, diagnose it, fix the owner/mode, and run a small Python web app. No cloud account or paid services are required.

## Before you start

Use a disposable **Ubuntu 24.04** VM, or Ubuntu 24.04 on WSL2. On macOS, use a Linux VM: these administrative commands are not macOS commands. Use your own account with sudo access. Do not run the setup on a shared university server. The username `cloudstudent` and `/srv/cloud-lab` must not already be in use by unrelated work.

Install prerequisites if needed:

```bash
sudo apt-get update
sudo apt-get install -y python3 curl procps passwd
```

Extract `linux-permissions-lab.zip` into your **Linux home directory** so you have `~/linux-permissions-lab/app.py`. Under WSL, copy the extracted folder into your Linux home and work there, rather than under `/mnt/c`; Windows filesystem permissions behave differently. No Python packages are required. In the recording, `learner` is the normal administrative account. Your own username and numeric IDs may differ.

Sudo may ask for **your own password**. Nothing appears while you type. The isolated recording container has a lab-only passwordless sudo setup to avoid recording credentials. You do not need to configure passwordless sudo on your laptop.

## 1. Verify your starting point

```bash
cd ~/linux-permissions-lab
ls
python3 --version
whoami
```

Expect `app.py`, `README.md`, Python 3.x, and your own normal username. The application responds with `Hello, cloud students!` at `/` and `OK` at `/health`. It binds to **127.0.0.1:8000 inside Linux**. This is a local teaching service, not a production server.

## 2. Create the deliberate mistake

Run once in your disposable lab. If `cloudstudent` already exists, check whether you have already completed setup; do not delete or reuse an unrelated account.

```bash
sudo useradd -m -U -s /bin/bash cloudstudent
id cloudstudent
sudo install -d -m 755 -o cloudstudent -g cloudstudent /srv/cloud-lab
sudo cp app.py /srv/cloud-lab/app.py
sudo chown root:root /srv/cloud-lab/app.py
sudo chmod 600 /srv/cloud-lab/app.py
sudo -u cloudstudent python3 /srv/cloud-lab/app.py
```

**Expected failure:** Python cannot open the file: `Permission denied` (exit status 2). The server has not started. This is intentional.

## 3. Diagnose, fix and verify

```bash
ls -l /srv/cloud-lab/app.py
ls -ld /srv/cloud-lab
sudo chown cloudstudent:cloudstudent /srv/cloud-lab/app.py
sudo chmod 640 /srv/cloud-lab/app.py
ls -l /srv/cloud-lab/app.py
```

Before the fix: `root root`, mode `-rw-------`. After: `cloudstudent cloudstudent`, mode `-rw-r-----`. The directory must also be traversable. Directory `x` means traversal/search. Do not use `chmod 777` or recursive changes to system paths.

## 4. Run and check the app

```bash
sudo -iu cloudstudent
cd /srv/cloud-lab
python3 app.py >app.log 2>&1 & app_pid=$!
curl --fail --silent http://127.0.0.1:8000/
curl --fail --silent http://127.0.0.1:8000/health
ps -p "$app_pid" -o pid,user,stat,args
cat app.log
```

Expect the greeting and `OK`. Keep this terminal open: `app_pid` is a **shell variable**, not a permanent service manager. Do not copy a PID from the video. Confirm user and command before signaling a process. Under this loopback setup, run curl in the same Linux environment; a host-laptop browser is a separate context.

## 5. Answer the Short's question

```bash
chmod 600 app.py
kill -TERM "$app_pid"
# Wait a moment for the old process to stop.
python3 app.py >app.log 2>&1 & app_pid=$!
curl --fail --silent http://127.0.0.1:8000/health
kill -TERM "$app_pid"
exit
```

Expect `OK` after restart. The owner can still read the file with mode 600. When you invoke `python3 app.py`, Python reads the source file; its own executable runs, so the source file does not need `x`. Exit returns to your original account. A “Terminated” job notification is normal after stopping the server.

## 6. Independent exercise

Return to cloudstudent and `/srv/cloud-lab`. Change `app.py` to **400**. Predict whether the app will run, whether cloudstudent can edit the source, and why. Start it, check `/health`, inspect its PID, and stop it. Try writing a harmless comment to the file and explain the result. Restore mode 640 after the exercise. See `SOLUTION.md` only after making your prediction.

## If your output differs

- Missing directory: check the archive extraction location, then repeat `cd`.
- Missing Python or curl: install the prerequisites above.
- Permission error during the first run: expected; continue with diagnosis.
- Permission error after the fix: check `id`, file ownership/mode, and directory traversal permissions.
- Connection refused: read `app.log`; the process may have exited. Check `ps` and the current user/path.
- Address already in use: inspect the existing listener (`sudo ss -ltnp 'sport = :8000'`). Identify it before stopping anything. Do not kill unrelated processes. Alternatively run `PORT=8001 python3 app.py` and use that port in curl.
- `app_pid` empty in a new shell: return to the original shell or identify the process with `ps -u cloudstudent -o pid,user,args`; verify the command before stopping it.

## Official references

- https://manpages.ubuntu.com/manpages/noble/man8/useradd.8.html
- https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html
- https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html
- https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html
- https://manpages.ubuntu.com/manpages/noble/man1/ps.1.html
- https://www.gnu.org/software/bash/manual/html_node/Job-Control-Builtins.html
- https://docs.python.org/3.12/library/http.server.html
