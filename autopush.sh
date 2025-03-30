#!/bin/bash
./test_all.sh
if [ $? -eq 0 ]; then
  git add .
  git commit -m "[loop success] Recursive cycle passed at $(date)"
  git push origin main
else
  echo "[❌] Tests failed. Push aborted."
  exit 1
fi
