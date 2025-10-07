# File Organizer CLI

A Python command-line utility that automatically organizes files in a directory by categorizing them based on their file types. Perfect for cleaning up messy Downloads folders or any directory with mixed file types.

## Features

- Automatically categorize files by type (Images, Documents, Videos, Audio, Archives, Code, Executables)
- Dry-run mode to preview changes before applying
- Undo functionality to reverse the last organization
- Handles duplicate filenames gracefully
- Detailed operation logging
- Simple and intuitive CLI interface
- Cross-platform support (Windows, macOS, Linux)

## File Categories

The organizer sorts files into the following categories:

- **Images**: .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico, .tiff
- **Documents**: .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx, .csv
- **Videos**: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpeg
- **Audio**: .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a, .opus
- **Archives**: .zip, .rar, .7z, .tar, .gz, .bz2, .xz, .iso
- **Code**: .py, .js, .java, .cpp, .c, .h, .cs, .php, .rb, .go, .rs, .swift
- **Executables**: .exe, .msi, .dmg, .deb, .rpm, .app, .bat, .sh
- **Others**: Any file type not listed above

## Installation

### Option 1: Direct Download

1. Download the `file_organizer.py` script
2. Ensure you have Python 3.6 or higher installed
3. Run the script directly (no additional dependencies required)

### Option 2: Clone the Repository

```bash
git clone https://github.com/AdityaDwiNugroho/HACKTOBERFEST_25_Python.git
cd HACKTOBERFEST_25_Python/File-Organizer
```

## Usage

### Basic Usage

Organize the current directory:
```bash
python file_organizer.py .
```

Organize a specific directory:
```bash
python file_organizer.py /path/to/messy/folder
```

### Dry Run Mode

Preview what would happen without actually moving files:
```bash
python file_organizer.py /path/to/folder --dry-run
```

This is highly recommended before organizing important directories.

### Undo Operation

Reverse the last organization operation:
```bash
python file_organizer.py /path/to/folder --undo
```

## Examples

### Example 1: Organize Downloads Folder

Before:
```
Downloads/
  report.pdf
  photo.jpg
  music.mp3
  video.mp4
  document.docx
  archive.zip
```

After running `python file_organizer.py ~/Downloads`:
```
Downloads/
  Documents/
    report.pdf
    document.docx
  Images/
    photo.jpg
  Audio/
    music.mp3
  Videos/
    video.mp4
  Archives/
    archive.zip
```

### Example 2: Preview Changes

```bash
$ python file_organizer.py . --dry-run

DRY RUN - Organizing 15 files in: /home/user/downloads

  [PREVIEW] report.pdf                 -> Documents/report.pdf
  [PREVIEW] photo.jpg                  -> Images/photo.jpg
  [PREVIEW] music.mp3                  -> Audio/music.mp3
  ...

==================================================
ORGANIZATION SUMMARY
==================================================
  Audio                :   3 files
  Documents            :   5 files
  Images               :   4 files
  Videos               :   2 files
  Archives             :   1 files
==================================================
  Total Organized      :  15 files
==================================================

This was a dry run. No files were moved.
Run without --dry-run to actually organize files.
```

### Example 3: Undo Organization

```bash
$ python file_organizer.py . --undo

Undoing last organization (15 files)...

  [RESTORED] report.pdf
  [RESTORED] photo.jpg
  [RESTORED] music.mp3
  ...

Restored 15 files.
```

## How It Works

1. **Scanning**: The script scans the specified directory for all files (not subdirectories)
2. **Categorization**: Each file is categorized based on its extension
3. **Organization**: Files are moved into category-specific folders
4. **Logging**: All operations are logged to `.file_organizer_log.json` for undo functionality
5. **Duplicate Handling**: If a file with the same name exists, a counter is added (e.g., `file_1.pdf`)

## Safety Features

- **Dry Run Mode**: Test before making changes
- **Operation Logging**: Every move is logged for potential recovery
- **Undo Support**: Easily reverse the last organization
- **Duplicate Protection**: Never overwrites existing files
- **Error Handling**: Skips problematic files and continues operation

## Command-Line Options

```
usage: file_organizer.py [-h] [--dry-run] [--undo] [directory]

Organize files in a directory by type

positional arguments:
  directory   Directory to organize (default: current directory)

optional arguments:
  -h, --help  show this help message and exit
  --dry-run   Preview changes without moving files
  --undo      Undo the last organization operation
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Contributing

This project was created as part of Hacktoberfest 2025. Contributions are welcome!

To contribute:
1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

Possible improvements:
- Add custom category definitions
- Support for organizing by date/size
- Interactive mode with user prompts
- Configuration file support
- Recursive directory organization
- Progress bar for large operations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Contributed for Hacktoberfest 2025

## Troubleshooting

### Permission Errors
If you get permission errors, make sure you have read/write access to the directory you're trying to organize.

### Files Not Moving
Check that the files aren't currently in use by another program.

### Undo Not Working
The undo feature requires the `.file_organizer_log.json` file created during organization. If this file is deleted, undo will not work.

## Changelog

### Version 1.0.0 (October 2025)
- Initial release
- Basic file organization by type
- Dry-run mode
- Undo functionality
- Duplicate filename handling
- Operation logging
