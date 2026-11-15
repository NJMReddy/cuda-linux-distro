#!/usr/bin/env python3
"""Bounded serial boot smoke test. Login alone never implies full readiness."""
import datetime, json, os, pathlib, re, subprocess, sys, time
root=pathlib.Path(__file__).resolve().parents[1]
logs=root/'boot-logs'; logs.mkdir(exist_ok=True)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
serial=logs/f'serial-{stamp}.log'; serial.touch()
env=dict(os.environ,SERIAL_LOG=str(serial))
start=time.monotonic(); p=subprocess.Popen(['bash',str(root/'scripts/run-qemu.sh')],env=env)
result={'status':'FAIL','scope':'QEMU firmware/kernel/init smoke only','serial':str(serial),'runtime_controls':'NOT TESTED','gpu':'BLOCKED'}
try:
    while time.monotonic()-start<float(os.environ.get('BOOT_TIMEOUT','180')):
        text=serial.read_text(errors='replace')
        if re.search(r'cuda-distro login:\s*$',text):
            result['boot_to_login_ms']=round((time.monotonic()-start)*1000)
            if re.search(r'Kernel panic|failed to mount|ERROR:.*failed|\[ !! \]',text,re.I):
                result['reason']='critical boot error in serial log'
            else: result['status']='PASS'
            break
        if p.poll() is not None:
            result['reason']=f'QEMU exited before login ({p.returncode})'; break
        time.sleep(.1)
    else: result['reason']='timeout before actual login prompt'
finally:
    if p.poll() is None:
        p.terminate()
        try: p.wait(timeout=5)
        except subprocess.TimeoutExpired: p.kill(); p.wait()
(logs/f'boot-{stamp}.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2)); sys.exit(result['status']!='PASS')
