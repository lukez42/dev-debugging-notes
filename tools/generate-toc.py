#!/usr/bin/env python3
"""
tools/generate-toc.py - Generate Table of Contents for markdown files

This script automatically generates a table of contents for markdown files
based on their header structure. It can process individual files or entire
directories.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class TOCGenerator:
    def __init__(self):
        self.header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.existing_toc_pattern = re.compile(
            r'<!-- TOC START -->.*?<!-- TOC END -->', 
            re.DOTALL
        )
    
    def extract_headers(self, content: str) -> List[Tuple[int, str, str]]:
        """Extract headers from markdown content.
        
        Returns:
            List of tuples: (level, title, anchor)
        """
        headers = []
        matches = self.header_pattern.findall(content)
        
        for match in matches:
            level = len(match[0])  # Number of # characters
            title = match[1].strip()
            
            # Skip if it's already a TOC header
            if title.lower() in ['table of contents', 'contents', 'toc']:
                continue
                
            # Generate anchor (GitHub style)
            anchor = self.generate_anchor(title)
            headers.append((level, title, anchor))
        
        return headers
    
    def generate_anchor(self, title: str) -> str:
        """Generate GitHub-style anchor from title."""
        # Convert to lowercase
        anchor = title.lower()
        
        # Replace spaces and special chars with hyphens
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)
        
        # Remove multiple consecutive hyphens
        anchor = re.sub(r'-+', '-', anchor)
        
        # Remove leading/trailing hyphens
        anchor = anchor.strip('-')
        
        return anchor
    
    def generate_toc(self, headers: List[Tuple[int, str, str]], 
                     max_depth: int = 6, min_depth: int = 1) -> str:
        """Generate TOC string from headers."""
        if not headers:
            return ""
        
        toc_lines = ["<!-- TOC START -->", "## Table of Contents", ""]
        
        # Find the minimum level to normalize indentation
        min_level = min(level for level, _, _ in headers)
        
        for level, title, anchor in headers:
            # Skip headers outside the specified depth range
            if level < min_depth or level > max_depth:
                continue
            
            # Calculate indentation (normalize to start at 0)
            indent_level = level - min_level
            indent = "  " * indent_level
            
            # Create the TOC entry
            toc_entry = f"{indent}- [{title}](#{anchor})"
            toc_lines.append(toc_entry)
        
        toc_lines.extend(["", "<!-- TOC END -->", ""])
        return "\n".join(toc_lines)
    
    def update_file_toc(self, file_path: Path, max_depth: int = 6, 
                        min_depth: int = 1, insert_after: str = None) -> bool:
        """Update TOC in a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract headers
            headers = self.extract_headers(content)
            
            if not headers:
                print(f"⚠️  No headers found in {file_path}")
                return False
            
            # Generate new TOC
            new_toc = self.generate_toc(headers, max_depth, min_depth)
            
            # Check if TOC already exists
            if self.existing_toc_pattern.search(content):
                # Replace existing TOC
                updated_content = self.existing_toc_pattern.sub(new_toc, content)
                print(f"🔄 Updated existing TOC in {file_path}")
            else:
                # Insert new TOC
                if insert_after:
                    # Insert after specified text
                    pattern = re.compile(re.escape(insert_after), re.IGNORECASE)
                    if pattern.search(content):
                        updated_content = pattern.sub(
                            f"{insert_after}\n\n{new_toc}", content, count=1
                        )
                    else:
                        # Insert at beginning if pattern not found
                        updated_content = f"{new_toc}\n{content}"
                else:
                    # Insert at the beginning
                    updated_content = f"{new_toc}\n{content}"
                print(f"✅ Added new TOC to {file_path}")
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return False
    
    def generate_repo_index(self, repo_path: Path) -> Dict[str, List[str]]:
        """Generate an index of all issues in the repository."""
        index = {
            'quick-reference': [],
            'detailed-guides': [],
            'platform-specific': []
        }
        
        for category in index.keys():
            category_path = repo_path / category
            if not category_path.exists():
                continue
            
            # Find all markdown files
            for md_file in category_path.rglob('*.md'):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract issue titles (headers starting with ##)
                    issue_pattern = re.compile(r'^## (.+)$', re.MULTILINE)
                    issues = issue_pattern.findall(content)
                    
                    for issue in issues:
                        # Create relative path for link
                        rel_path = md_file.relative_to(repo_path)
                        anchor = self.generate_anchor(issue)
                        link = f"[{issue}]({rel_path}#{anchor})"
                        index[category].append(link)
                        
                except Exception as e:
                    print(f"⚠️  Error reading {md_file}: {e}")
        
        return index
    
    def update_main_readme(self, repo_path: Path) -> bool:
        """Update the main README with current repository index."""
        readme_path = repo_path / 'README.md'
        if not readme_path.exists():
            print(f"❌ README.md not found at {readme_path}")
            return False
        
        # Generate current index
        index = self.generate_repo_index(repo_path)
        
        # Count statistics
        total_issues = sum(len(issues) for issues in index.values())
        quick_fixes = len(index['quick-reference'])
        detailed_guides = len(index['detailed-guides'])
        platform_specific = len(index['platform-specific'])
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update statistics
            stats_pattern = re.compile(
                r'- \*\*Total Issues:\*\* \d+\n'
                r'- \*\*Quick Fixes:\*\* \d+\n'
                r'- \*\*Detailed Guides:\*\* \d+',
                re.MULTILINE
            )
            
            new_stats = (
                f"- **Total Issues:** {total_issues}\n"
                f"- **Quick Fixes:** {quick_fixes}\n"
                f"- **Detailed Guides:** {detailed_guides}"
            )
            
            if stats_pattern.search(content):
                updated_content = stats_pattern.sub(new_stats, content)
                print(f"🔄 Updated statistics in README.md")
            else:
                print(f"⚠️  Could not find statistics section in README.md")
                return False
            
            # Update last updated date
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            date_pattern = re.compile(r'- \*\*Last Updated:\*\* \d{4}-\d{2}-\d{2}')
            new_date = f"- **Last Updated:** {today}"
            
            if date_pattern.search(updated_content):
                updated_content = date_pattern.sub(new_date, updated_content)
            
            # Write back
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Updated README.md with current statistics")
            return True
            
        except Exception as e:
            print(f"❌ Error updating README.md: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate Table of Contents for markdown files"
    )
    parser.add_argument(
        'path', 
        help='Path to markdown file or directory'
    )
    parser.add_argument(
        '--max-depth', 
        type=int, 
        default=6,
        help='Maximum header depth to include (default: 6)'
    )
    parser.add_argument(
        '--min-depth', 
        type=int, 
        default=1,
        help='Minimum header depth to include (default: 1)'
    )
    parser.add_argument(
        '--insert-after',
        help='Insert TOC after this text (for new files)'
    )
    parser.add_argument(
        '--update-readme',
        action='store_true',
        help='Update main README.md with current repository statistics'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Process all markdown files in directory recursively'
    )
    
    args = parser.parse_args()
    
    generator = TOCGenerator()
    path = Path(args.path)
    
    if args.update_readme:
        # Update main README with repository statistics
        if generator.update_main_readme(path):
            print("🎉 README.md updated successfully!")
        return
    
    if not path.exists():
        print(f"❌ Path does not exist: {path}")
        sys.exit(1)
    
    success_count = 0
    total_count = 0
    
    if path.is_file():
        # Process single file
        if path.suffix.lower() == '.md':
            total_count = 1
            if generator.update_file_toc(
                path, 
                args.max_depth, 
                args.min_depth, 
                args.insert_after
            ):
                success_count = 1
        else:
            print(f"❌ File is not a markdown file: {path}")
            sys.exit(1)
    
    elif path.is_dir():
        # Process directory
        if args.recursive:
            md_files = list(path.rglob('*.md'))
        else:
            md_files = list(path.glob('*.md'))
        
        total_count = len(md_files)
        
        if total_count == 0:
            print(f"⚠️  No markdown files found in {path}")
            return
        
        print(f"🔍 Found {total_count} markdown files")
        
        for md_file in md_files:
            if generator.update_file_toc(
                md_file, 
                args.max_depth, 
                args.min_depth, 
                args.insert_after
            ):
                success_count += 1
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Processed: {success_count}/{total_count} files")
    
    if success_count == total_count:
        print("🎉 All files processed successfully!")
    elif success_count > 0:
        print("⚠️  Some files had issues")
    else:
        print("❌ No files were processed successfully")


if __name__ == "__main__":
    main()