#!/bin/bash
# tools/search-issues.sh - Search through debugging issues

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

usage() {
    echo -e "${BLUE}Usage: $0 [OPTIONS] SEARCH_TERM${NC}"
    echo ""
    echo "Search through debugging issues and solutions"
    echo ""
    echo "Options:"
    echo "  -t, --tag TAG         Search by tag (#quick-fix, #macos, etc.)"
    echo "  -c, --category CAT    Search in specific category (vscode, git, etc.)"
    echo "  -f, --files-only      Show only matching filenames"
    echo "  -n, --no-content      Don't show content preview"
    echo "  -i, --case-sensitive  Case sensitive search"
    echo "  -h, --help           Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 \"conda PATH\"                    # Search for conda PATH issues"
    echo "  $0 -t \"#quick-fix\" python         # Quick fixes for Python"
    echo "  $0 -c vscode \"terminal\"           # VSCode terminal issues"
    echo "  $0 -f docker                       # Files mentioning docker"
}

# Default values
SEARCH_TERM=""
TAG=""
CATEGORY=""
FILES_ONLY=0
NO_CONTENT=0
CASE_SENSITIVE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -c|--category)
            CATEGORY="$2"
            shift 2
            ;;
        -f|--files-only)
            FILES_ONLY=1
            shift
            ;;
        -n|--no-content)
            NO_CONTENT=1
            shift
            ;;
        -i|--case-sensitive)
            CASE_SENSITIVE=""
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            exit 1
            ;;
        *)
            SEARCH_TERM="$1"
            shift
            ;;
    esac
done

# Set case sensitivity
if [[ -z "$CASE_SENSITIVE" ]]; then
    GREP_OPTS="-i"
else
    GREP_OPTS=""
fi

# Build search path
if [[ -n "$CATEGORY" ]]; then
    SEARCH_PATH="quick-reference/${CATEGORY}.md platform-specific/${CATEGORY}.md detailed-guides/*${CATEGORY}*"
else
    SEARCH_PATH="quick-reference/ platform-specific/ detailed-guides/"
fi

# Function to search by tag
search_by_tag() {
    local tag="$1"
    echo -e "${YELLOW}🏷️  Searching for tag: ${tag}${NC}"
    echo ""
    
    find $SEARCH_PATH -name "*.md" 2>/dev/null | while read -r file; do
        if grep -q $GREP_OPTS "$tag" "$file" 2>/dev/null; then
            echo -e "${GREEN}📄 $(basename "$file")${NC}"
            if [[ $FILES_ONLY -eq 0 && $NO_CONTENT -eq 0 ]]; then
                # Show the issue title and first few lines
                grep -A 3 -B 1 $GREP_OPTS "$tag" "$file" | head -10
                echo ""
            fi
        fi
    done
}

# Function to search by term
search_by_term() {
    local term="$1"
    echo -e "${YELLOW}🔍 Searching for: ${term}${NC}"
    echo ""
    
    local found=0
    find $SEARCH_PATH -name "*.md" 2>/dev/null | while read -r file; do
        if grep -q $GREP_OPTS "$term" "$file" 2>/dev/null; then
            found=1
            echo -e "${GREEN}📄 $(basename "$(dirname "$file")")/$(basename "$file")${NC}"
            
            if [[ $FILES_ONLY -eq 0 ]]; then
                # Show matching lines with context
                if [[ $NO_CONTENT -eq 0 ]]; then
                    echo -e "${BLUE}---${NC}"
                    grep -n -A 2 -B 1 $GREP_OPTS --color=always "$term" "$file" 2>/dev/null | head -10
                    echo ""
                fi
            fi
        fi
    done
    
    if [[ $found -eq 0 ]]; then
        echo -e "${RED}No results found.${NC}"
    fi
}

# Function to show popular searches
show_popular() {
    echo -e "${YELLOW}🔥 Popular Searches:${NC}"
    echo ""
    echo -e "${BLUE}Common Issues:${NC}"
    echo "  ./search-issues.sh \"PATH\""
    echo "  ./search-issues.sh \"conda\""
    echo "  ./search-issues.sh \"git authentication\""
    echo "  ./search-issues.sh \"docker permission\""
    echo ""
    echo -e "${BLUE}By Tags:${NC}"
    echo "  ./search-issues.sh -t \"#quick-fix\""
    echo "  ./search-issues.sh -t \"#macos\""
    echo "  ./search-issues.sh -t \"#environment\""
    echo ""
    echo -e "${BLUE}By Category:${NC}"
    echo "  ./search-issues.sh -c vscode"
    echo "  ./search-issues.sh -c python"
    echo "  ./search-issues.sh -c git"
}

# Main logic
if [[ -n "$TAG" ]]; then
    search_by_tag "$TAG"
elif [[ -n "$SEARCH_TERM" ]]; then
    search_by_term "$SEARCH_TERM"
else
    show_popular
fi

# Show statistics
echo -e "${BLUE}---${NC}"
TOTAL_FILES=$(find quick-reference/ platform-specific/ detailed-guides/ -name "*.md" 2>/dev/null | wc -l)
echo -e "${BLUE}📊 Total files searched: ${TOTAL_FILES}${NC}"