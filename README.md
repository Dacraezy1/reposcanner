# RepoScanner

RepoScanner is a secure Linux tool designed to analyze GitHub repositories for potential security concerns in shell scripts and Python files. While primarily developed for Arch Linux, it's compatible with other Linux distributions.

## Features

- 🔍 Recursively scans repositories for `.sh` and `.py` files
- ⚡ Fast and efficient analysis
- 🛡️ Read-only operations (safe to run on any repository)
- 🚨 Detects potentially unsafe patterns:
  - Dangerous shell commands (`rm -rf`, etc.)
  - Suspicious Python patterns (`eval`, `exec`, etc.)
  - Uncommented privileged operations
- 📊 Generates comprehensive summary reports

## Installation

### Prerequisites

- Python 3.8 or higher
- Git

### Basic Installation

1. Clone the repository:
```bash
git clone https://github.com/Dacraezy1/reposcanner.git
cd reposcanner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Scan a single repository:
```bash
./scan_repo.py /path/to/repository
```

Scan multiple repositories:
```bash
./scan_repo.py /path/to/repo1 /path/to/repo2
```

### Options

```bash
-v, --verbose     Enable verbose output
-r, --report      Generate detailed HTML report
-p, --patterns    Path to custom pattern file
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests (`python -m pytest tests/`)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## Security

RepoScanner is designed to be read-only and safe to run. It never executes any code from the scanned repositories.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
