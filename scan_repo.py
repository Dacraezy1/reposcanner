#!/usr/bin/env python3

import os
import sys
import re
import argparse
from typing import List, Dict, Set
from pathlib import Path
import json
from datetime import datetime

class RepoScanner:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.dangerous_patterns = {
            'shell': [
                (r'rm\s+-rf\s+[/]*', 'Dangerous recursive removal'),
                (r'chmod\s+777', 'Overly permissive file permissions'),
                (r'curl\s+.*\s+\|\s+bash', 'Piping curl to bash'),
                (r'wget\s+.*\s+\|\s+bash', 'Piping wget to bash'),
            ],
            'python': [
                (r'eval\(', 'Use of eval()'),
                (r'exec\(', 'Use of exec()'),
                (r'os\.system\(', 'Direct system command execution'),
                (r'subprocess\.call\([^,]*shell=True', 'Shell=True in subprocess'),
                (r'input\(', 'Use of input() - consider argparse'),
            ]
        }
        self.stats = {
            'total_files': 0,
            'shell_scripts': 0,
            'python_files': 0,
            'issues_found': 0,
        }

    def scan_file(self, file_path: Path) -> List[Dict]:
        """
        Scan a single file for dangerous patterns.
        """
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            patterns = (self.dangerous_patterns['shell'] 
                       if file_path.suffix == '.sh' 
                       else self.dangerous_patterns['python'])
            
            for pattern, description in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    issues.append({
                        'file': str(file_path),
                        'line': content.count('\n', 0, match.start()) + 1,
                        'pattern': pattern,
                        'description': description,
                        'context': content.splitlines()[content.count('\n', 0, match.start())]
                    })
            
        except Exception as e:
            if self.verbose:
                print(f"Error scanning {file_path}: {e}")
        
        return issues

    def scan_repository(self, repo_path: Path) -> Dict:
        """
        Scan an entire repository for shell and Python files.
        """
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")

        all_issues = []
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in ['.sh', '.py']:
                    self.stats['total_files'] += 1
                    if file_path.suffix == '.sh':
                        self.stats['shell_scripts'] += 1
                    else:
                        self.stats['python_files'] += 1
                    
                    issues = self.scan_file(file_path)
                    all_issues.extend(issues)
                    self.stats['issues_found'] += len(issues)

        return {
            'repository': str(repo_path),
            'timestamp': datetime.now().isoformat(),
            'statistics': self.stats,
            'issues': all_issues
        }

def main():
    parser = argparse.ArgumentParser(
        description='Scan GitHub repositories for potentially dangerous patterns'
    )
    parser.add_argument('paths', nargs='+', help='Paths to repositories to scan')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-o', '--output', help='Output JSON file for results')
    args = parser.parse_args()

    scanner = RepoScanner(verbose=args.verbose)
    all_results = []

    for repo_path in args.paths:
        try:
            results = scanner.scan_repository(Path(repo_path))
            all_results.append(results)
            
            # Print summary
            print(f"\nResults for {repo_path}:")
            print(f"Files scanned: {results['statistics']['total_files']}")
            print(f"Shell scripts: {results['statistics']['shell_scripts']}")
            print(f"Python files: {results['statistics']['python_files']}")
            print(f"Issues found: {results['statistics']['issues_found']}")
            
            if results['issues']:
                print("\nPotential issues:")
                for issue in results['issues']:
                    print(f"\n{issue['file']}:{issue['line']}")
                    print(f"Warning: {issue['description']}")
                    print(f"Context: {issue['context'].strip()}")
            
        except Exception as e:
            print(f"Error scanning {repo_path}: {e}", file=sys.stderr)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(all_results, f, indent=2)

if __name__ == '__main__':
    main()