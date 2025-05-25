#!/usr/bin/env python3

import os
import re
from datetime import datetime
from pathlib import Path

def count_issues_in_file(file_path):
    """Count the number of issues in a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Count sections that start with ## (excluding the first one which is usually the title)
        sections = re.findall(r'^##\s+', content, re.MULTILINE)
        return len(sections) - 1 if sections else 0

def count_quick_fixes():
    """Count quick fixes in quick-reference directory."""
    total = 0
    for file in Path('quick-reference').glob('*.md'):
        total += count_issues_in_file(file)
    return total

def count_detailed_guides():
    """Count detailed guides in detailed-guides directory."""
    total = 0
    for file in Path('detailed-guides').rglob('*.md'):
        total += count_issues_in_file(file)
    return total

def update_readme_stats():
    """Update the statistics section in README.md."""
    quick_fixes = count_quick_fixes()
    detailed_guides = count_detailed_guides()
    total_issues = quick_fixes + detailed_guides
    last_updated = datetime.now().strftime('%Y-%m-%d')

    # Read the current README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Update the statistics section
    stats_pattern = r'## Statistics\n\n(.*?)(?=\n##|\Z)'
    new_stats = f"""## Statistics

- **Total Issues:** {total_issues}
- **Quick Fixes:** {quick_fixes}
- **Detailed Guides:** {detailed_guides}
- **Last Updated:** {last_updated}
"""

    # Replace the statistics section
    if re.search(stats_pattern, content, re.DOTALL):
        new_content = re.sub(stats_pattern, new_stats, content, flags=re.DOTALL)
    else:
        # If statistics section doesn't exist, add it before the last section
        sections = content.split('\n## ')
        if len(sections) > 1:
            sections.insert(-1, new_stats.lstrip('## '))
            new_content = '\n## '.join(sections)
        else:
            new_content = content + '\n' + new_stats

    # Write the updated content
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Statistics updated:")
    print(f"- Total Issues: {total_issues}")
    print(f"- Quick Fixes: {quick_fixes}")
    print(f"- Detailed Guides: {detailed_guides}")
    print(f"- Last Updated: {last_updated}")

if __name__ == '__main__':
    update_readme_stats() 