import pytest
from pathlib import Path
from scan_repo import RepoScanner

def test_scanner_initialization():
    scanner = RepoScanner()
    assert scanner.stats['total_files'] == 0
    assert scanner.stats['issues_found'] == 0

def test_dangerous_patterns_loaded():
    scanner = RepoScanner()
    assert 'shell' in scanner.dangerous_patterns
    assert 'python' in scanner.dangerous_patterns
    assert len(scanner.dangerous_patterns['shell']) > 0
    assert len(scanner.dangerous_patterns['python']) > 0

def test_scan_nonexistent_path():
    scanner = RepoScanner()
    with pytest.raises(ValueError):
        scanner.scan_repository(Path('/nonexistent/path'))