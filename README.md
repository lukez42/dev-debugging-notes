# dev-debugging-notes

A comprehensive collection of common development debugging issues and their solutions.

## Repository Structure

```
dev-debugging-notes/
├── README.md                 # This file - main index
├── quick-reference/          # One-liner fixes
│   ├── vscode.md
│   ├── git.md
│   ├── python.md
│   └── node.md
├── detailed-guides/          # Step-by-step solutions
│   ├── environment-setup/
│   ├── database-issues/
│   ├── deployment-problems/
│   └── performance-debugging/
├── platform-specific/        # OS-specific issues
│   ├── macos.md
│   ├── windows.md
│   └── linux.md
├── tools/                    # Helper scripts
│   ├── add-issue.sh
│   ├── search-issues.sh
│   ├── generate-toc.py
│   └── update-stats.py
└── templates/                # Issue templates
    ├── quick-fix.md
    └── detailed-guide.md
```

## Quick Search

**Most Common Issues:**
- [VSCode Python/Conda PATH Issues](#vscode)
- [Git Authentication Problems](#git)
- [Node Package Manager Conflicts](#node)
- [Database Connection Timeouts](#database)

## Categories

### VSCode
| Issue | Type | Platform | Link |
|-------|------|----------|------|
| Conda PATH not working | Environment | macOS | [→](quick-reference/vscode.md#conda-path-issue) |
| Python interpreter not switching | Environment | All | [→](quick-reference/vscode.md#python-interpreter) |
| Terminal inheritance problems | Configuration | macOS | [→](quick-reference/vscode.md#terminal-inheritance) |

### Git
| Issue | Type | Platform | Link |
|-------|------|----------|------|
| SSH key authentication | Authentication | All | [→](quick-reference/git.md#ssh-auth) |
| Merge conflicts | Workflow | All | [→](quick-reference/git.md#merge-conflicts) |
| Large file handling | Performance | All | [→](detailed-guides/git-lfs.md) |

### Python/Conda
| Issue | Type | Platform | Link |
|-------|------|----------|------|
| Package installation conflicts | Dependencies | All | [→](quick-reference/python.md#package-conflicts) |
| Virtual environment activation | Environment | All | [→](quick-reference/python.md#venv-activation) |
| Import path issues | Configuration | All | [→](quick-reference/python.md#import-paths) |

### Node/NPM
| Issue | Type | Platform | Link |
|-------|------|----------|------|
| NPM vs Yarn vs PNPM conflicts | Package Manager | All | [→](quick-reference/node.md#package-manager-conflicts) |
| Node version switching | Environment | All | [→](quick-reference/node.md#node-version) |
| Permission errors | Installation | macOS/Linux | [→](quick-reference/node.md#permissions) |

## Usage

### Quick Reference
For immediate fixes, check the `quick-reference/` folder:
```bash
# Search for a specific issue
grep -r "conda PATH" quick-reference/
```

### Detailed Guides
For complex problems requiring multiple steps, see `detailed-guides/`.

### Adding New Issues
Use the provided script:
```bash
./tools/add-issue.sh "VSCode Python PATH" "quick-reference/vscode.md"
```

## Tools

The `tools/` directory contains helper scripts to manage and search through the debugging notes:

### 1. add-issue.sh
Adds new issues to the repository with proper formatting and metadata.
```bash
# Add a quick fix
./tools/add-issue.sh "Issue Title" "quick-reference/category.md"

# Add a detailed guide
./tools/add-issue.sh "Issue Title" "detailed-guides/category/guide.md" --detailed

# Options:
#   --detailed    Create a detailed guide instead of a quick fix
#   --platform    Specify platform (macos, windows, linux, all)
#   --tags        Add custom tags (comma-separated)
```

### 2. search-issues.sh
Searches through all issues using various criteria.
```bash
# Search by keyword
./tools/search-issues.sh "memory leak"

# Search by tag
./tools/search-issues.sh --tag "performance"

# Search by platform
./tools/search-issues.sh --platform "macos"

# Options:
#   --tag         Filter by tag
#   --platform    Filter by platform
#   --type        Filter by type (quick-fix, detailed-guide)
#   --category    Filter by category (e.g., database, deployment)
```

### 3. update-stats.py
Updates the statistics in README.md based on current repository state.
```bash
# Update statistics
python3 tools/update-stats.py

# This will automatically update:
# - Total number of issues
# - Number of quick fixes
# - Number of detailed guides
# - Last updated date
```

### 4. generate-toc.py
Generates a table of contents for markdown files (coming soon).
```bash
# Generate TOC for a specific file
python3 tools/generate-toc.py path/to/file.md

# Generate TOC for all files in a directory
python3 tools/generate-toc.py path/to/directory/
```

## Statistics

- **Total Issues:** 36
- **Quick Fixes:** 8
- **Detailed Guides:** 28
- **Last Updated:** 2025-05-25

## Tags

Issues are tagged for easy filtering:
- `#quick-fix` - Single command/setting solutions
- `#step-by-step` - Multi-step procedures  
- `#platform-specific` - OS-dependent solutions
- `#configuration` - Settings/config file changes
- `#environment` - PATH, variables, package managers
- `#authentication` - SSH, tokens, passwords
- `#performance` - Speed, memory, optimization issues

---
`
**Tip:** Use `Cmd+F` (or `Ctrl+F`) to search within this README, or use the search scripts in `tools/` for repo-wide searches.