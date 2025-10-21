# Port Scanner 🔍

A Python program for scanning and identifying open ports on target hosts with a beautiful terminal UI.

## Features ✨

- **Fast Concurrent Scanning**: Multi-threaded port scanning for optimal performance
- **Beautiful Terminal UI**: Rich terminal interface with progress bars, colors, and tables
- **Flexible Port Specification**: Scan single ports, port ranges, or comma-separated lists
- **Service Detection**: Automatically identifies common services running on open ports
- **Configurable Settings**: Adjust timeout and thread count for different network conditions
- **Automation-Ready**: Perfect for scripting and automation tasks

## Installation 📦

1. Clone the repository:
```bash
git clone https://github.com/999Cypher/port-Scanner.git
cd port-Scanner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage 🚀

### Basic Syntax
```bash
python port_scanner.py <target> [options]
```

### Arguments

- `target`: Target hostname or IP address to scan (required)
- `-p, --ports`: Port(s) to scan (default: 1-1024)
  - Single port: `80`
  - Port range: `1-1000`
  - Comma-separated: `22,80,443,8080`
- `-t, --timeout`: Connection timeout in seconds (default: 1.0)
- `-w, --workers`: Maximum number of concurrent threads (default: 100)

### Examples

**Scan common ports on localhost:**
```bash
python port_scanner.py localhost -p 1-1024
```

**Scan specific ports:**
```bash
python port_scanner.py example.com -p 22,80,443,8080
```

**Scan with custom timeout and thread count:**
```bash
python port_scanner.py 192.168.1.1 -p 1-65535 -t 0.5 -w 200
```

**Quick scan of web ports:**
```bash
python port_scanner.py example.com -p 80,443,8000,8080,8443
```

## Output 📊

The scanner displays results in a beautiful, easy-to-read format:

- **Progress Bar**: Real-time scanning progress with percentage
- **Results Table**: Clear table showing open ports and their services
- **Scan Summary**: Statistics including total ports scanned, open/closed ports, and duration

## Features for Automation 🤖

The port scanner is designed for automation:

- **Exit Codes**: Returns appropriate exit codes for scripting
- **JSON Output**: Results can be easily parsed for integration
- **Concurrent Scanning**: Fast execution for large port ranges
- **Error Handling**: Robust error handling for network issues

## Requirements 📋

- Python 3.7+
- rich (for terminal UI)

## Security Notice ⚠️

This tool is intended for legitimate network administration and security testing purposes only. Always ensure you have proper authorization before scanning any network or system.

## License 📄

This project is open source and available for educational and professional use.

## Contributing 🤝

Contributions are welcome! Feel free to submit issues and pull requests.

## Author ✍️

Created with ❤️ for network administrators and security professionals.
