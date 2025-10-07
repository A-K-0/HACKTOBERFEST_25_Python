"""
File Organizer CLI - Automatically organize files by type

A command-line utility that organizes messy directories by sorting files
into categorized folders based on their extensions.
"""

import os
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set


class FileOrganizer:
    
    FILE_CATEGORIES = {
        'Images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'},
        'Documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'},
        'Videos': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg'},
        'Audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus'},
        'Archives': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'},
        'Code': {'.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.swift'},
        'Executables': {'.exe', '.msi', '.dmg', '.deb', '.rpm', '.app', '.bat', '.sh'},
        'Others': set()
    }
    
    def __init__(self, target_dir: str, dry_run: bool = False):
        self.target_dir = Path(target_dir).resolve()
        self.dry_run = dry_run
        self.operations_log: List[Dict] = []
        self.log_file = self.target_dir / '.file_organizer_log.json'
        
        if not self.target_dir.exists():
            raise ValueError(f"Directory does not exist: {target_dir}")
        
        if not self.target_dir.is_dir():
            raise ValueError(f"Path is not a directory: {target_dir}")
    
    def get_category(self, file_path: Path) -> str:
        extension = file_path.suffix.lower()
        
        for category, extensions in self.FILE_CATEGORIES.items():
            if extension in extensions:
                return category
        
        return 'Others'
    
    def get_unique_filename(self, destination: Path) -> Path:
        if not destination.exists():
            return destination
        
        base = destination.stem
        extension = destination.suffix
        counter = 1
        
        while True:
            new_name = f"{base}_{counter}{extension}"
            new_path = destination.parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def organize(self) -> Dict[str, int]:
        stats = {category: 0 for category in self.FILE_CATEGORIES.keys()}
        skipped = 0
        
        files = [f for f in self.target_dir.iterdir() if f.is_file()]
        files = [f for f in files if f.name != '.file_organizer_log.json']
        
        print(f"\n{'DRY RUN - ' if self.dry_run else ''}Organizing {len(files)} files in: {self.target_dir}\n")
        
        for file_path in files:
            try:
                category = self.get_category(file_path)
                category_dir = self.target_dir / category
                
                if not self.dry_run and not category_dir.exists():
                    category_dir.mkdir(parents=True, exist_ok=True)
                
                destination = category_dir / file_path.name
                destination = self.get_unique_filename(destination)
                
                operation = {
                    'timestamp': datetime.now().isoformat(),
                    'source': str(file_path),
                    'destination': str(destination),
                    'category': category
                }
                
                if self.dry_run:
                    print(f"  [PREVIEW] {file_path.name:40} -> {category}/{destination.name}")
                else:
                    shutil.move(str(file_path), str(destination))
                    self.operations_log.append(operation)
                    print(f"  [MOVED] {file_path.name:40} -> {category}/{destination.name}")
                
                stats[category] += 1
                
            except Exception as e:
                print(f"  [ERROR] Failed to move {file_path.name}: {e}")
                skipped += 1
        
        if not self.dry_run and self.operations_log:
            self._save_log()
        
        stats['Skipped'] = skipped
        return stats
    
    def _save_log(self):
        try:
            existing_log = []
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    existing_log = json.load(f)
            
            existing_log.extend(self.operations_log)
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(existing_log, f, indent=2, ensure_ascii=False)
            
            print(f"\nOperations logged to: {self.log_file}")
            
        except Exception as e:
            print(f"Warning: Could not save log file: {e}")
    
    def undo(self) -> int:
        if not self.log_file.exists():
            print("No operations log found. Nothing to undo.")
            return 0
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                operations = json.load(f)
            
            if not operations:
                print("No operations to undo.")
                return 0
            
            print(f"\nUndoing last organization ({len(operations)} files)...\n")
            
            restored = 0
            for operation in reversed(operations):
                try:
                    source = Path(operation['destination'])
                    destination = Path(operation['source'])
                    
                    if source.exists():
                        shutil.move(str(source), str(destination))
                        print(f"  [RESTORED] {source.name}")
                        restored += 1
                    else:
                        print(f"  [SKIP] File not found: {source.name}")
                        
                except Exception as e:
                    print(f"  [ERROR] Failed to restore {source.name}: {e}")
            
            for category in self.FILE_CATEGORIES.keys():
                category_dir = self.target_dir / category
                if category_dir.exists() and not any(category_dir.iterdir()):
                    category_dir.rmdir()
                    print(f"  [REMOVED] Empty directory: {category}")
            
            self.log_file.unlink()
            print(f"\nRestored {restored} files.")
            return restored
            
        except Exception as e:
            print(f"Error during undo operation: {e}")
            return 0


def print_statistics(stats: Dict[str, int]):
    print("\n" + "=" * 50)
    print("ORGANIZATION SUMMARY")
    print("=" * 50)
    
    total = sum(v for k, v in stats.items() if k != 'Skipped')
    
    for category, count in sorted(stats.items()):
        if count > 0:
            print(f"  {category:20} : {count:3} files")
    
    print("=" * 50)
    print(f"  {'Total Organized':20} : {total:3} files")
    print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Organize files in a directory by type',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Organize current directory:
    python file_organizer.py .
    
  Preview organization without moving files:
    python file_organizer.py /path/to/folder --dry-run
    
  Undo last organization:
    python file_organizer.py /path/to/folder --undo
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to organize (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without moving files'
    )
    
    parser.add_argument(
        '--undo',
        action='store_true',
        help='Undo the last organization operation'
    )
    
    args = parser.parse_args()
    
    try:
        organizer = FileOrganizer(args.directory, dry_run=args.dry_run)
        
        if args.undo:
            organizer.undo()
        else:
            stats = organizer.organize()
            print_statistics(stats)
            
            if args.dry_run:
                print("This was a dry run. No files were moved.")
                print("Run without --dry-run to actually organize files.\n")
        
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
