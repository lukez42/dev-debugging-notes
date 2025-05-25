#!/bin/bash
# tools/add-issue.sh - Script to add new debugging issues

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${BLUE}Usage: $0 [OPTIONS]${NC}"
    echo ""
    echo "Add a new debugging issue to the repository"
    echo ""
    echo "Options:"
    echo "  -t, --title TITLE      Issue title (required)"
    echo "  -f, --file FILE        Target file (e.g., quick-reference/vscode.md)"
    echo "  -c, --category CAT     Category (vscode, git, python, node, etc.)"
    echo "  -g, --tags TAGS        Comma-separated tags (#quick-fix, #macos, etc.)"
    echo "  -i, --interactive      Interactive mode"
    echo "  -h, --help            Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 -t \"Docker port binding\" -c docker -g \"#quick-fix,#networking\""
    echo "  $0 -i  # Interactive mode"
}

# Interactive mode function
interactive_mode() {
    echo -e "${BLUE}🔧 Interactive Issue Addition${NC}"
    echo ""
    
    # Get title
    read -p "Issue title: " TITLE
    [ -z "$TITLE" ] && { echo -e "${RED}Title is required${NC}"; exit 1; }
    
    # Get category
    echo ""
    echo "Available categories:"
    echo "  1) vscode    2) git       3) python    4) node"
    echo "  5) docker    6) database  7) macos     8) linux"
    echo "  9) windows   10) other"
    echo ""
    read -p "Select category (1-10): " CAT_NUM
    
    case $CAT_NUM in
        1) CATEGORY="vscode" ;;
        2) CATEGORY="git" ;;
        3) CATEGORY="python" ;;
        4) CATEGORY="node" ;;
        5) CATEGORY="docker" ;;
        6) CATEGORY="database" ;;
        7) CATEGORY="macos" ;;
        8) CATEGORY="linux" ;;
        9) CATEGORY="windows" ;;
        10) CATEGORY="other" ;;
        *) CATEGORY="other" ;;
    esac
    
    # Get tags
    echo ""
    echo "Common tags: #quick-fix #step-by-step #configuration #environment #performance"
    read -p "Tags (comma-separated): " TAGS
    
    # Determine file
    if [[ "$CATEGORY" == "macos" || "$CATEGORY" == "linux" || "$CATEGORY" == "windows" ]]; then
        FILE="platform-specific/${CATEGORY}.md"
    else
        FILE="quick-reference/${CATEGORY}.md"
    fi
    
    echo ""
    echo -e "${YELLOW}Summary:${NC}"
    echo "  Title: $TITLE"
    echo "  Category: $CATEGORY"
    echo "  File: $FILE"
    echo "  Tags: $TAGS"
    echo ""
    read -p "Continue? (y/N): " CONFIRM
    [[ ! "$CONFIRM" =~ ^[Yy]$ ]] && { echo "Cancelled."; exit 0; }
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--title)
            TITLE="$2"
            shift 2
            ;;
        -f|--file)
            FILE="$2"
            shift 2
            ;;
        -c|--category)
            CATEGORY="$2"
            shift 2
            ;;
        -g|--tags)
            TAGS="$2"
            shift 2
            ;;
        -i|--interactive)
            INTERACTIVE=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            exit 1
            ;;
    esac
done

# Run interactive mode if requested
if [[ "$INTERACTIVE" == "1" ]]; then
    interactive_mode
fi

# Validate required arguments
if [[ -z "$TITLE" ]]; then
    echo -e "${RED}Error: Title is required${NC}"
    usage
    exit 1
fi

# Set default values
CATEGORY="${CATEGORY:-other}"
FILE="${FILE:-quick-reference/${CATEGORY}.md}"
TAGS="${TAGS:-#quick-fix}"

# Create directory if it doesn't exist
DIR=$(dirname "$FILE")
mkdir -p "$DIR"

# Generate issue ID (lowercase, hyphens)
ISSUE_ID=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

# Create issue template
TEMPLATE="
## $ISSUE_ID

**Problem:** $TITLE  
**Tags:** \`$TAGS\`

**Quick Fix:**
\`\`\`bash
# Add your solution here
\`\`\`

**Example:**
\`\`\`bash
# Before (broken):

# After (working):
\`\`\`

---
"

# Add to file
if [[ -f "$FILE" ]]; then
    echo "$TEMPLATE" >> "$FILE"
else
    echo "# $(basename "$FILE" .md | tr '[:lower:]' '[:upper:]') Quick Reference" > "$FILE"
    echo "$TEMPLATE" >> "$FILE"
fi

# Update main README stats (basic increment)
if [[ -f "README.md" ]]; then
    # This is a simple increment - you might want to make this more sophisticated
    CURRENT_COUNT=$(grep "Total Issues:" README.md | grep -o '[0-9]\+' || echo "0")
    NEW_COUNT=$((CURRENT_COUNT + 1))
    sed -i.bak "s/Total Issues.*$/Total Issues:** $NEW_COUNT/" README.md
    rm README.md.bak 2>/dev/null || true
fi

echo -e "${GREEN}✅ Issue added successfully!${NC}"
echo -e "${BLUE}📁 File: $FILE${NC}"
echo -e "${BLUE}🔖 Issue ID: $ISSUE_ID${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit $FILE to add the actual solution"
echo "2. Update README.md with the new issue link"
echo "3. Commit your changes"
echo ""
echo -e "${BLUE}Edit now? (y/N):${NC}"
read -r EDIT
if [[ "$EDIT" =~ ^[Yy]$ ]]; then
    ${EDITOR:-code} "$FILE"
fi