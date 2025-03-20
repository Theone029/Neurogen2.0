#!/usr/bin/env python3
import os, time, subprocess, psutil
script_name = os.path.basename(__file__)
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if script_name in ' '.join(proc.info.get('cmdline', [])) and proc.info['pid'] != os.getpid():
        print(f"{script_name} is already running. Exiting...")
        exit()

SCRIPTS = [
    "process_watchdog.py",
    "system_monitor.py",
    "log_ai_analyzer.py",
    "task_watcher.py",
    "notifier_bot.py"
]

def check_and_restart(script):
    try:
        result = subprocess.run(["pgrep", "-f", script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{script} is not running. Restarting...")
            # Restart using the virtualenv interpreter and log the output
            subprocess.Popen("nohup neurogen_env/bin/python3 " + script + " > logs/" + script + ".log 2>&1 &", shell=True)
    except Exception as e:
        print(f"Error checking {script}: {e}")

while True:
    for script in SCRIPTS:
        check_and_restart(script)
    time.sleep(60)  # Check every 60 seconds
