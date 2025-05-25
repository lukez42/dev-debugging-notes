# macOS Development Guide

## Common Issues and Solutions

### Homebrew
- **Issue**: Package installation fails
- **Fix**: 
  ```bash
  brew update
  brew upgrade
  brew doctor
  ```

### Permissions
- **Issue**: Permission denied errors
- **Fix**: 
  ```bash
  # Fix ownership
  sudo chown -R $(whoami) /usr/local/*
  # Fix permissions
  chmod +x script.sh
  ```

### Port Conflicts
- **Issue**: Port already in use
- **Fix**: 
  ```bash
  # Find process using port
  lsof -i :3000
  # Kill process
  kill -9 <PID>
  ```

## Development Tools
- Xcode Command Line Tools
- Homebrew
- iTerm2
- VS Code

## Environment Setup
```bash
# Install Xcode CLI tools
xcode-select --install

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Common development tools
brew install git node python@3.9
``` 