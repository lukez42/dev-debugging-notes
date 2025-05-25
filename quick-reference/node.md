# Node.js Quick Reference

## Common Issues and Solutions

### Module Resolution
- **Issue**: Cannot find module
- **Fix**: 
  - Check package.json dependencies
  - Run `npm install`
  - Clear node_modules: `rm -rf node_modules && npm install`

### Memory Issues
- **Issue**: JavaScript heap out of memory
- **Fix**: 
  ```bash
  # Increase heap size
  export NODE_OPTIONS="--max-old-space-size=4096"
  # or
  node --max-old-space-size=4096 script.js
  ```

### NPM Issues
- **Issue**: NPM install fails
- **Fix**: 
  - Clear cache: `npm cache clean --force`
  - Delete package-lock.json
  - Use `npm ci` instead of `npm install`

## Common Commands
```bash
# Package management
npm install
npm update
npm audit fix

# Development
npm run dev
npm run build
npm run test

# Debugging
node --inspect script.js
# or
node --inspect-brk script.js
```

## Environment Variables
- Use `.env` file with `dotenv` package
- Never commit `.env` to version control
- Use `.env.example` as template 