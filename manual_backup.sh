#!/bin/bash
# NEUROGATE Manual Backup Script
# This script stages all changes, commits them, pushes to the remote repo,
# and tags the commit for future restoration.

echo "Staging all changes..."
git add .

read -p "Enter commit message (default: [manual save] stable recursive milestone backup): " commit_msg
if [ -z "\$commit_msg" ]; then
  commit_msg="[manual save] stable recursive milestone backup"
fi

echo "Committing changes..."
git commit -m "\$commit_msg"

echo "Pushing changes to origin..."
git push

read -p "Enter tag (default: v1.0-recursive-stable): " tag_name
if [ -z "\$tag_name" ]; then
  tag_name="v1.0-recursive-stable"
fi

echo "Tagging commit as \$tag_name..."
git tag "\$tag_name"
git push origin "\$tag_name"

echo "Backup complete."
