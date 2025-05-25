# Python Quick Reference

## Common Issues and Solutions

### Virtual Environment
- **Issue**: Package conflicts or wrong Python version
- **Fix**: 
  ```bash
  python -m venv venv
  source venv/bin/activate  # Unix
  .\venv\Scripts\activate   # Windows
  ```

### Import Errors
- **Issue**: ModuleNotFoundError
- **Fix**: 
  - Check PYTHONPATH
  - Install missing package: `pip install package-name`
  - Use relative imports: `from .module import function`

### Debugging
- **Issue**: Need to debug code
- **Fix**: 
  ```python
  import pdb; pdb.set_trace()  # Add breakpoint
  # or
  breakpoint()  # Python 3.7+
  ```

## Common Commands
```bash
# Package management
pip install -r requirements.txt
pip freeze > requirements.txt
pip list --outdated

# Running tests
python -m pytest
python -m unittest

# Code quality
python -m black .
python -m flake8
python -m mypy .
``` 