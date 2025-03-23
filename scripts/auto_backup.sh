#!/bin/bash

# === AUTO BACKUP SCRIPT W/ COMMIT LOGGING ===

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
CHANGED=$(git status --porcelain)
if [ -z "$CHANGED" ]; then
  echo "⚠️  No changes to commit."
  exit 0
fi

# Commit message (manual override or default)
MSG=${1:-"Auto Backup @ $TIMESTAMP"}

echo "Committing with message: $MSG"
git add .
git commit -m "$MSG"
git push origin main

# Log it to logs/commits.md
echo -e "\n## [$TIMESTAMP] $MSG\n" >> logs/commits.md
git diff HEAD~1 --name-status >> logs/commits.md

echo "✅ Auto-backup complete."
