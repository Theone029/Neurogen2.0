#!/usr/bin/env python3
import psutil, os
script_name = os.path.basename(__file__)
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if script_name in ' '.join(proc.info.get('cmdline', [])) and proc.info['pid'] != os.getpid():
        print(f"{script_name} is already running. Exiting...")
        exit()
# Insert your process monitoring logic here
print("Process Watchdog running...")
