#!/bin/bash
# This script applies permanent fixes for PostgreSQL and SSH configurations.
# Run it as root: sudo bash fix_configs.sh

# Ensure the script is run as root.
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (e.g., sudo bash $0)"
  exit 1
fi

echo "Applying PostgreSQL configuration fixes..."

# PostgreSQL configuration file paths (adjust version if needed)
PG_CONF="/etc/postgresql/14/main/postgresql.conf"
PG_HBA="/etc/postgresql/14/main/pg_hba.conf"

# Update postgresql.conf: set listen_addresses to 'localhost'
if [ -f "$PG_CONF" ]; then
  # Uncomment and set listen_addresses to 'localhost'
  sed -i "s/^#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" "$PG_CONF"
  sed -i "s/^listen_addresses = .*/listen_addresses = 'localhost'/" "$PG_CONF"
  echo "Set listen_addresses to 'localhost' in $PG_CONF"
else
  echo "Warning: $PG_CONF not found."
fi

# Update pg_hba.conf: ensure local IPv4 and IPv6 connections are allowed via md5 authentication
if [ -f "$PG_HBA" ]; then
  # Append the lines if they are not already present.
  grep -qE "^host\s+all\s+all\s+127\.0\.0\.1/32\s+md5" "$PG_HBA" || echo "host    all             all             127.0.0.1/32            md5" >> "$PG_HBA"
  grep -qE "^host\s+all\s+all\s+::1/128\s+md5" "$PG_HBA" || echo "host    all             all             ::1/128                 md5" >> "$PG_HBA"
  echo "Ensured local connections are allowed in $PG_HBA"
else
  echo "Warning: $PG_HBA not found."
fi

# Restart PostgreSQL
echo "Restarting PostgreSQL..."
systemctl restart postgresql && echo "PostgreSQL restarted." || { echo "Failed to restart PostgreSQL."; exit 1; }

echo ""
echo "Applying SSH configuration fixes..."

# SSH configuration file path
SSH_CONF="/etc/ssh/sshd_config"
DESIRED_SSH_PORT=2222  # Change this value if you prefer a different port

if [ -f "$SSH_CONF" ]; then
  # Back up the original SSH configuration
  cp "$SSH_CONF" "${SSH_CONF}.bak"
  echo "Backed up SSH config to ${SSH_CONF}.bak"
  
  # Update the Port setting: uncomment if necessary and set it to DESIRED_SSH_PORT
  sed -i "s/^#Port .*/Port ${DESIRED_SSH_PORT}/" "$SSH_CONF"
  sed -i "s/^Port .*/Port ${DESIRED_SSH_PORT}/" "$SSH_CONF"
  echo "Set SSH port to ${DESIRED_SSH_PORT} in $SSH_CONF"
else
  echo "Warning: $SSH_CONF not found."
fi

# Restart SSH service (the service may be named sshd or ssh, adjust if necessary)
if systemctl list-units --type=service | grep -q "sshd.service"; then
  systemctl restart sshd && echo "SSH service (sshd) restarted." || echo "Failed to restart sshd."
else
  systemctl restart ssh && echo "SSH service (ssh) restarted." || echo "Failed to restart ssh."
fi

# Adjust UFW (if active) to allow the desired SSH port
if ufw status | grep -qi "Status: active"; then
  ufw allow "${DESIRED_SSH_PORT}/tcp"
  ufw reload
  echo "UFW rule added to allow port ${DESIRED_SSH_PORT}/tcp"
fi

echo ""
echo "Permanent fixes applied. Please test PostgreSQL and SSH connections."

