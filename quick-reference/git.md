# Git Quick Reference

## Common Issues and Solutions

### Authentication
- **Issue**: Authentication failures
- **Fix**: 
  - Check SSH keys: `ssh -T git@github.com`
  - Update credentials: `git config --global credential.helper store`

### Merge Conflicts
- **Issue**: Merge conflicts during pull/merge
- **Fix**: 
  - Resolve conflicts in editor
  - Use `git mergetool`
  - After resolving: `git add . && git commit`

### Stashing
- **Issue**: Need to temporarily save changes
- **Fix**: 
  - Save: `git stash save "message"`
  - Apply: `git stash pop`
  - List: `git stash list`

## Common Commands
```bash
# Basic workflow
git status
git add .
git commit -m "message"
git push

# Branch management
git checkout -b new-branch
git branch -d branch-name
git merge branch-name

# History
git log --oneline
git log --graph --oneline --all
``` 