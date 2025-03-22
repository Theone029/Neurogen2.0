#!/bin/bash
#
# auto_backup.sh
#
# A robust script to automatically stage, commit, and push changes to the repository.
# It categorizes code changes into system modules, auto-generates commit messages,
# and supports optional manual override.
#
# Why It Works for NEUROGEN:
# - Atomic commits: Categorizes changes by folder, mirroring your architecture.
# - Auto-generated messages: Standardizes logs for both human tracking and AI parsing.
# - Manual override: Supply your own message when needed.
# - Date-stamped fallback: Provides context even for changes outside known directories.
# - Optional auto-tagging: Tags major updates if the commit message signals a big update.
# - Auto-log: Appends commit history to logs/commits.md for a persistent changelog.
#
# Usage:
#   bash auto_backup.sh             # Auto-generates a commit message.
#   bash auto_backup.sh "Custom commit message"   # Uses your custom message.
#

# Check for git command availability.
if ! command -v git &>/dev/null; then
    echo "Error: git is not installed. Please install git to continue."
    exit 1
fi

# Navigate to the project root (assumes this script is in the 'scripts' folder).
cd "$(dirname "$0")/.." || { echo "Error: Unable to change directory."; exit 1; }

# Stage all changes.
git add .

# Check if there are any changes to commit.
if git diff-index --quiet HEAD --; then
    echo "No changes to commit."
    exit 0
fi

# Determine commit message.
if [ -z "$1" ]; then
    # Auto-generate commit message based on changed file paths.
    CHANGED_FILES=$(git diff --cached --name-only)
    COMMIT_MSG="Update: "
    if echo "$CHANGED_FILES" | grep -q "^core/"; then
        COMMIT_MSG+="core module updated; "
    fi
    if echo "$CHANGED_FILES" | grep -q "^config/"; then
        COMMIT_MSG+="configuration tweaked; "
    fi
    if echo "$CHANGED_FILES" | grep -q "^scripts/"; then
        COMMIT_MSG+="scripts enhanced; "
    fi
    if echo "$CHANGED_FILES" | grep -q "^docker/"; then
        COMMIT_MSG+="docker setup refined; "
    fi
    if echo "$CHANGED_FILES" | grep -q "^data/"; then
        COMMIT_MSG+="data samples adjusted; "
    fi
    if echo "$CHANGED_FILES" | grep -q "^logs/"; then
        COMMIT_MSG+="logs maintained; "
    fi
    if echo "$CHANGED_FILES" | grep -q "README.md"; then
        COMMIT_MSG+="README improved; "
    fi
    # Fallback if no known directories are touched.
    if [ "$COMMIT_MSG" = "Update: " ]; then
        COMMIT_MSG="Update on $(date '+%Y-%m-%d %H:%M:%S'): Minor tweaks."
    else
        # Remove trailing semicolon and space.
        COMMIT_MSG=$(echo "$COMMIT_MSG" | sed 's/; $//')
    fi
else
    COMMIT_MSG="$1"
fi

echo "Committing with message: $COMMIT_MSG"

# Commit changes.
git commit -m "$COMMIT_MSG"
COMMIT_STATUS=$?
if [ $COMMIT_STATUS -ne 0 ]; then
    echo "❌ Commit failed. Aborting auto-backup."
    exit 1
fi

# Optional: Auto-tag major updates if commit message contains "major update".
if echo "$COMMIT_MSG" | grep -qi "major update"; then
    TAG_NAME="v$(date '+%Y.%m.%d')"
    git tag -a "$TAG_NAME" -m "Auto-tagged commit: $COMMIT_MSG"
    echo "Tagged commit with $TAG_NAME"
fi

# Determine current branch.
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" = "HEAD" ]; then
    echo "Warning: Detached HEAD state. Pushing might not work as expected."
fi

# Push changes.
git push origin "$CURRENT_BRANCH"
PUSH_STATUS=$?

# Optional: Append commit details to logs/commits.md.
mkdir -p logs
LOG_FILE="logs/commits.md"
echo "- $(date '+%Y-%m-%d %H:%M:%S'): $COMMIT_MSG" >> "$LOG_FILE"

if [ $PUSH_STATUS -eq 0 ]; then
    echo "✅ Auto-backup complete."
    exit 0
else
    echo "❌ Git push may have failed. Check network or token."
    exit 1
fi
