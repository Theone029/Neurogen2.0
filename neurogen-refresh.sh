#!/bin/bash
echo "í´ Restarting NEUROGEN components..."

# Restart memory container
sudo fuser -k 8001/tcp
docker build -t neurogen-memory .
docker stop neurogen-memory
docker rm neurogen-memory
docker run -d --name neurogen-memory -p 8001:8001 neurogen-memory

# Restart Discord bot
pkill -f bot.py
nohup python3 bot.py > logs/bot.log 2>&1 &

echo "âœ… NEUROGEN core refreshed."

