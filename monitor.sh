#\!/bin/bash
while true; do
  if ! pgrep -f NeuroStrike.py >/dev/null; then
    echo "[RECOVERY] NeuroStrike.py down. Relaunching..."
    nohup python3 ~/neurogen/NeuroStrike.py > ~/neurogen/logs/nohup.out 2>&1 &
  fi
  sleep 10
done
