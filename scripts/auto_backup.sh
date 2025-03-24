#!/bin/bash
set -euo pipefail

# Directories to ensure are tracked even if empty
DIRECTORIES=("logs" "core" "scripts" "data" "config")

for dir in "\${DIRECTORIES[@]}"; do
    if [ -d "\$dir" ]; then
        if [ -z "\$(ls -A "\$dir")" ]; then
            echo "Directory \$dir is empty, adding .gitkeep."
            touch "\$dir/.gitkeep"
        fi
    fi
done

# Stage all changes
git add .

# Check if there are any changes to commit
if git diff-index --quiet HEAD --; then
    echo "No changes to commit."
    exit 0
fi

# Use the provided commit message or a default timestamped message
COMMIT_MSG=\${1:-"Auto Backup \$(date +'%Y-%m-%d %H:%M:%S')"}
echo "Committing with message: \$COMMIT_MSG"
git commit -m "\$COMMIT_MSG"

# Push to the main branch
git push origin main
echo "Auto-backup complete."
