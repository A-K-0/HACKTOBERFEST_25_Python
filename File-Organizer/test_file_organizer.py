"""
Unit tests for File Organizer CLI

Run tests with: pytest test_file_organizer.py
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import json
from file_organizer import FileOrganizer


class TestFileOrganizer:
    """Test suite for FileOrganizer class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def sample_files(self, temp_dir):
        """Create sample files for testing."""
        files = {
            'document.pdf': 'Documents',
            'image.jpg': 'Images',
            'video.mp4': 'Videos',
            'audio.mp3': 'Audio',
            'archive.zip': 'Archives',
            'script.py': 'Code',
            'unknown.xyz': 'Others'
        }
        
        for filename in files.keys():
            (temp_dir / filename).touch()
        
        return files
    
    def test_initialization_valid_directory(self, temp_dir):
        """Test FileOrganizer initialization with valid directory."""
        organizer = FileOrganizer(str(temp_dir))
        assert organizer.target_dir == temp_dir
        assert organizer.dry_run is False
    
    def test_initialization_invalid_directory(self):
        """Test FileOrganizer initialization with invalid directory."""
        with pytest.raises(ValueError, match="Directory does not exist"):
            FileOrganizer("/nonexistent/directory")
    
    def test_initialization_file_instead_of_directory(self, temp_dir):
        """Test FileOrganizer initialization with file path instead of directory."""
        file_path = temp_dir / "test.txt"
        file_path.touch()
        
        with pytest.raises(ValueError, match="Path is not a directory"):
            FileOrganizer(str(file_path))
    
    def test_get_category_image(self, temp_dir):
        """Test category detection for image files."""
        organizer = FileOrganizer(str(temp_dir))
        
        assert organizer.get_category(Path("photo.jpg")) == "Images"
        assert organizer.get_category(Path("picture.png")) == "Images"
        assert organizer.get_category(Path("icon.svg")) == "Images"
    
    def test_get_category_document(self, temp_dir):
        """Test category detection for document files."""
        organizer = FileOrganizer(str(temp_dir))
        
        assert organizer.get_category(Path("report.pdf")) == "Documents"
        assert organizer.get_category(Path("letter.docx")) == "Documents"
        assert organizer.get_category(Path("data.xlsx")) == "Documents"
    
    def test_get_category_video(self, temp_dir):
        """Test category detection for video files."""
        organizer = FileOrganizer(str(temp_dir))
        
        assert organizer.get_category(Path("movie.mp4")) == "Videos"
        assert organizer.get_category(Path("clip.avi")) == "Videos"
        assert organizer.get_category(Path("video.mkv")) == "Videos"
    
    def test_get_category_audio(self, temp_dir):
        """Test category detection for audio files."""
        organizer = FileOrganizer(str(temp_dir))
        
        assert organizer.get_category(Path("song.mp3")) == "Audio"
        assert organizer.get_category(Path("track.wav")) == "Audio"
        assert organizer.get_category(Path("music.flac")) == "Audio"
    
    def test_get_category_code(self, temp_dir):
        """Test category detection for code files."""
        organizer = FileOrganizer(str(temp_dir))
        
        assert organizer.get_category(Path("script.py")) == "Code"
        assert organizer.get_category(Path("app.js")) == "Code"
        assert organizer.get_category(Path("main.cpp")) == "Code"
    
    def test_get_category_archive(self, temp_dir):
        """Test category detection for archive files."""
        organizer = FileOrganizer(str(temp_dir))
        
        assert organizer.get_category(Path("backup.zip")) == "Archives"
        assert organizer.get_category(Path("package.tar")) == "Archives"
        assert organizer.get_category(Path("compressed.7z")) == "Archives"
    
    def test_get_category_unknown(self, temp_dir):
        """Test category detection for unknown file types."""
        organizer = FileOrganizer(str(temp_dir))
        
        assert organizer.get_category(Path("unknown.xyz")) == "Others"
        assert organizer.get_category(Path("file.abc")) == "Others"
    
    def test_get_unique_filename_no_conflict(self, temp_dir):
        """Test unique filename generation when no conflict exists."""
        organizer = FileOrganizer(str(temp_dir))
        destination = temp_dir / "test.txt"
        
        result = organizer.get_unique_filename(destination)
        assert result == destination
    
    def test_get_unique_filename_with_conflict(self, temp_dir):
        """Test unique filename generation when conflict exists."""
        organizer = FileOrganizer(str(temp_dir))
        
        # Create conflicting files
        (temp_dir / "test.txt").touch()
        (temp_dir / "test_1.txt").touch()
        
        destination = temp_dir / "test.txt"
        result = organizer.get_unique_filename(destination)
        
        assert result == temp_dir / "test_2.txt"
    
    def test_dry_run_mode(self, temp_dir, sample_files):
        """Test that dry run mode doesn't move files."""
        organizer = FileOrganizer(str(temp_dir), dry_run=True)
        stats = organizer.organize()
        
        # Verify files are still in original location
        for filename in sample_files.keys():
            assert (temp_dir / filename).exists()
        
        # Verify no category directories were created
        for category in FileOrganizer.FILE_CATEGORIES.keys():
            if category != 'Others':
                assert not (temp_dir / category).exists()
        
        # Verify statistics were collected
        assert sum(stats.values()) > 0
    
    def test_organize_files(self, temp_dir, sample_files):
        """Test actual file organization."""
        organizer = FileOrganizer(str(temp_dir))
        stats = organizer.organize()
        
        # Verify files were moved to correct categories
        for filename, expected_category in sample_files.items():
            expected_path = temp_dir / expected_category / filename
            assert expected_path.exists(), f"{filename} not in {expected_category}"
            
            # Verify original file is gone
            assert not (temp_dir / filename).exists()
        
        # Verify statistics
        assert stats['Documents'] == 1
        assert stats['Images'] == 1
        assert stats['Videos'] == 1
        assert stats['Audio'] == 1
        assert stats['Archives'] == 1
        assert stats['Code'] == 1
        assert stats['Others'] == 1
    
    def test_organize_creates_log(self, temp_dir, sample_files):
        """Test that organization creates a log file."""
        organizer = FileOrganizer(str(temp_dir))
        organizer.organize()
        
        log_file = temp_dir / '.file_organizer_log.json'
        assert log_file.exists()
        
        # Verify log content
        with open(log_file, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
        
        assert len(log_data) == len(sample_files)
        assert all('source' in entry for entry in log_data)
        assert all('destination' in entry for entry in log_data)
        assert all('category' in entry for entry in log_data)
        assert all('timestamp' in entry for entry in log_data)
    
    def test_undo_operation(self, temp_dir, sample_files):
        """Test undo functionality."""
        organizer = FileOrganizer(str(temp_dir))
        
        # Organize files
        organizer.organize()
        
        # Verify files were moved
        for filename in sample_files.keys():
            assert not (temp_dir / filename).exists()
        
        # Undo operation
        restored = organizer.undo()
        
        # Verify files are back in original location
        for filename in sample_files.keys():
            assert (temp_dir / filename).exists()
        
        # Verify restoration count
        assert restored == len(sample_files)
        
        # Verify log file is removed
        log_file = temp_dir / '.file_organizer_log.json'
        assert not log_file.exists()
    
    def test_undo_removes_empty_directories(self, temp_dir, sample_files):
        """Test that undo removes empty category directories."""
        organizer = FileOrganizer(str(temp_dir))
        
        # Organize and then undo
        organizer.organize()
        organizer.undo()
        
        # Verify empty directories are removed
        for category in sample_files.values():
            category_dir = temp_dir / category
            assert not category_dir.exists() or any(category_dir.iterdir())
    
    def test_undo_without_log(self, temp_dir):
        """Test undo when no log file exists."""
        organizer = FileOrganizer(str(temp_dir))
        restored = organizer.undo()
        
        assert restored == 0
    
    def test_duplicate_filename_handling(self, temp_dir):
        """Test handling of duplicate filenames."""
        # Create two files with the same name in different locations
        (temp_dir / "test.pdf").touch()
        
        docs_dir = temp_dir / "Documents"
        docs_dir.mkdir()
        (docs_dir / "test.pdf").touch()
        
        organizer = FileOrganizer(str(temp_dir))
        organizer.organize()
        
        # Verify both files exist with different names
        assert (docs_dir / "test.pdf").exists()
        assert (docs_dir / "test_1.pdf").exists()
    
    def test_case_insensitive_extensions(self, temp_dir):
        """Test that file extensions are case-insensitive."""
        (temp_dir / "image.JPG").touch()
        (temp_dir / "document.PDF").touch()
        (temp_dir / "script.PY").touch()
        
        organizer = FileOrganizer(str(temp_dir))
        organizer.organize()
        
        assert (temp_dir / "Images" / "image.JPG").exists()
        assert (temp_dir / "Documents" / "document.PDF").exists()
        assert (temp_dir / "Code" / "script.PY").exists()
    
    def test_ignores_subdirectories(self, temp_dir):
        """Test that subdirectories are not organized."""
        # Create a subdirectory with files
        sub_dir = temp_dir / "subfolder"
        sub_dir.mkdir()
        (sub_dir / "test.txt").touch()
        
        # Create a file in main directory
        (temp_dir / "main.txt").touch()
        
        organizer = FileOrganizer(str(temp_dir))
        stats = organizer.organize()
        
        # Verify subdirectory still exists and wasn't moved
        assert sub_dir.exists()
        assert (sub_dir / "test.txt").exists()
        
        # Verify only main file was organized
        assert stats['Documents'] == 1
    
    def test_empty_directory(self, temp_dir):
        """Test organizing an empty directory."""
        organizer = FileOrganizer(str(temp_dir))
        stats = organizer.organize()
        
        # Verify no files were organized
        assert all(count == 0 for count in stats.values())
