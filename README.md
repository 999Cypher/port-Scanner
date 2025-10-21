⚡ Rich Port Scanner ⚡

A modern, fast, and feature-rich port scanner built with Python. This tool uses concurrent threading for high-speed scanning and the rich library to provide beautiful, easy-to-read terminal output.

Features

Concurrent Scanning: Utilizes a thread pool to scan multiple ports simultaneously for maximum speed.

Rich Terminal UI: Displays results in a clean, colorful table with a real-time progress bar.

Service & Banner Grabbing: Identifies common services and attempts to grab service banners for version identification.

Flexible CLI: Easy-to-use command-line arguments for specifying target, port range, timeout, and worker threads.

Directly Executable: Can be run as a standalone executable on Linux and macOS.

Installation & Setup

Clone the repository (or download the files):

# This is a hypothetical step for a real Git repo
git clone [https://github.com/your-username/rich-port-scanner.git](https://github.com/your-username/rich-port-scanner.git)
cd rich-port-scanner


Create a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


Install the required dependencies:

pip install -r requirements.txt


Make the script executable (for macOS/Linux users):

chmod +x port_scanner.py


Usage Examples

Once set up, you can run the scanner directly from your terminal.

1. Basic Scan (localhost on macOS/Linux):
To test the scanner on your own machine, scanning the first 100 ports with 50 workers:

./port_scanner.py 127.0.0.1 -p 1-100 -w 50


2. Basic Scan (Universal / Windows):
If the direct execution method doesn't work, or you're on Windows, use this command:

python port_scanner.py 127.0.0.1 -p 1-100 -w 50


3. Scan a Target on Your Network:
To scan a specific device on your home network for all well-known ports (1-1024) with 100 workers:

./port_scanner.py 192.168.1.10 -p 1-1024 -w 100


4. Scan a Specific Port Range:
To check only for common web ports on a target with a high number of workers:

./port_scanner.py example.com --ports 80,443,8000-8080 --workers 200


Command-Line Arguments

usage: port_scanner.py [-h] [-p PORTS] [-t TIMEOUT] [-w WORKERS] target

A cool and fast Python port scanner with a rich UI.

positional arguments:
  target                The IP address or hostname to scan.

options:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Port range to scan (e.g., '22-8080').
  -t TIMEOUT, --timeout TIMEOUT
                        Connection timeout in seconds for each port.
  -w WORKERS, --workers WORKERS
                        Number of concurrent threads (workers) to use.
