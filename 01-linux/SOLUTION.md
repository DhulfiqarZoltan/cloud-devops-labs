# Exercise solution — read after predicting

**Author:** Dr. Alwahab Dhulfiqar Zoltan

With `cloudstudent` as owner, mode **400** grants owner read permission but no write or execute permission. Group and others have no access. Python can read and run the source through `python3 app.py`. A write attempt by cloudstudent fails because the source is not writable. The directory must remain traversable. Root can bypass ordinary discretionary permission checks, so do not test the write as root.

```bash
sudo -iu cloudstudent
cd /srv/cloud-lab
chmod 400 app.py
python3 app.py >app.log 2>&1 & app_pid=$!
curl --fail --silent http://127.0.0.1:8000/health
ps -p "$app_pid" -o pid,user,stat,args
printf '# exercise\n' >> app.py
# Expected: Permission denied; no change is written.
kill -TERM "$app_pid"
chmod 640 app.py
exit
```

The current owner can change the file mode with chmod even when the file is not writable. This restores the intended exercise state.
