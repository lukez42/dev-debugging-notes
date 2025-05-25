# VSCode Quick Reference

## conda-path-issue

**Problem:** VSCode terminal shows different PATH than regular terminal, conda/pip not working  
**Tags:** `#quick-fix` `#environment` `#macos` `#configuration`

**Example Issue:**
```bash
# Regular Terminal (working) - base conda env activated:
(base) echo $PATH
/Users/luke/Library/pnpm:/opt/homebrew/opt/mysql-client/bin:/opt/anaconda3/bin:/opt/anaconda3/condabin:...
(base) which python
/opt/anaconda3/bin/python

# VSCode Terminal (broken) - base conda env activated:
(base) echo $PATH  
/opt/homebrew/opt/mysql-client/bin:/opt/homebrew/bin:...:/opt/anaconda3/bin:/opt/anaconda3/condabin
(base) which python
/opt/homebrew/bin/python  # Wrong! Should be conda's python
```

**Quick Fix:**
Add to VSCode `settings.json`:
```json
{
    "terminal.integrated.inheritEnv": false
}
```

**Access Settings:** `Cmd + ,` → Click `{}` icon → Add setting above

---

## python-interpreter

**Problem:** Python interpreter not auto-switching with conda environments  
**Tags:** `#configuration` `#environment` `#python`

**Quick Fix:**
```json
{
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.defaultInterpreterPath": "/opt/anaconda3/bin/python"
}
```

**Manual Override:** `Cmd+Shift+P` → "Python: Select Interpreter"

---

## terminal-inheritance

**Problem:** VSCode terminal inherits wrong environment from parent process  
**Tags:** `#quick-fix` `#macos` `#environment`

**Root Cause:** VSCode launched from Finder/Spotlight gets system PATH, not shell PATH

**Solutions:**
1. **Best:** `"terminal.integrated.inheritEnv": false`
2. **Alternative:** Always launch VSCode from terminal: `code /path/to/project`

---

## extensions-not-working

**Problem:** Extensions fail to load or work properly  
**Tags:** `#quick-fix` `#configuration`

**Quick Fixes:**
```bash
# Reload window
Cmd+Shift+P → "Developer: Reload Window"

# Reset extension host
Cmd+Shift+P → "Developer: Restart Extension Host"

# Clear extension cache
rm -rf ~/.vscode/extensions/.obsolete
```

---

## intellisense-slow

**Problem:** IntelliSense/autocomplete very slow or not working  
**Tags:** `#performance` `#python` `#configuration`

**Quick Fix:**
```json
{
    "python.analysis.autoImportCompletions": false,
    "python.analysis.indexing": false,
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/node_modules/**": true,
        "**/.venv/**": true
    }
}
```