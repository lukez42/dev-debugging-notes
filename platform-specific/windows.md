# Windows Development Guide

## Common Issues and Solutions

### Path Issues
- **Issue**: Command not found
- **Fix**: 
  - Add to PATH in System Properties
  - Use full paths
  - Check environment variables

### Line Endings
- **Issue**: CRLF vs LF conflicts
- **Fix**: 
  ```bash
  # Configure Git
  git config --global core.autocrlf true
  # or
  git config --global core.autocrlf input
  ```

### WSL
- **Issue**: Linux commands not working
- **Fix**: 
  - Install WSL: `wsl --install`
  - Update WSL: `wsl --update`
  - Set default version: `wsl --set-default-version 2`

## Development Tools
- Windows Terminal
- Git Bash
- WSL2
- VS Code with Remote WSL extension

## Environment Setup
```powershell
# Install Chocolatey (Package Manager)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install common tools
choco install git nodejs python vscode
``` 