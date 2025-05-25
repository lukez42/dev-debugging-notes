# Linux Development Guide

## Common Issues and Solutions

### Package Management
- **Issue**: Package installation fails
- **Fix**: 
  ```bash
  # Ubuntu/Debian
  sudo apt update
  sudo apt upgrade
  sudo apt install package-name

  # Fedora
  sudo dnf update
  sudo dnf install package-name
  ```

### Permissions
- **Issue**: Permission denied
- **Fix**: 
  ```bash
  # Fix ownership
  sudo chown -R $USER:$USER /path/to/directory
  # Fix permissions
  chmod +x script.sh
  # Add user to groups
  sudo usermod -aG docker $USER
  ```

### System Services
- **Issue**: Service won't start
- **Fix**: 
  ```bash
  # Check status
  sudo systemctl status service-name
  # View logs
  journalctl -u service-name
  # Restart service
  sudo systemctl restart service-name
  ```

## Development Tools
- Package managers (apt, dnf, pacman)
- Systemd
- Docker
- VS Code

## Environment Setup
```bash
# Update system
sudo apt update && sudo apt upgrade

# Install development tools
sudo apt install build-essential git curl

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install nodejs

# Install Python
sudo apt install python3 python3-pip python3-venv
``` 