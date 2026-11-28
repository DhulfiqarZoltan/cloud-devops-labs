# Independent exercise solution
Author: Dr. Alwahab Dhulfiqar Zoltan

Run in the extracted lab directory in the same Linux shell. Ensure the main example is stopped and no unrelated service owns either port.
```bash
PORT=8080 python3 app.py >exercise.log 2>&1 &
app_pid=$!
ps -p "$app_pid" -o pid,user,args
ss -ltnp 'sport = :8080'
curl --noproxy "*" --fail http://127.0.0.1:8080/health
curl --noproxy "*" --max-time 3 http://127.0.0.1:8000/health
# Previous curl should fail with exit 7 in this clean lab.
kill -TERM "$app_pid"; wait "$app_pid"; true
ss -ltn '( sport = :8000 or sport = :8080 )'
```
Allow a moment after launch if the first request races with startup. Inspect exercise.log if startup fails. Expected listener: 127.0.0.1:8080; health body: OK. Final socket listing has only the header. A client must target the address and port on which the server actually listens. PORT changes the app's listener; it does not change the default loopback bind.
