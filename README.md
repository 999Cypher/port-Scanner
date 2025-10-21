⚡ Rich Port Scanner ⚡

A modern, fast, and feature-rich port scanner built with Python. This tool uses concurrent threading for high-speed scanning and the rich library to provide beautiful, easy-to-read terminal output.

!

Features

Concurrent Scanning: Utilizes a thread pool to scan multiple ports simultaneously for maximum speed.

Rich Terminal UI: Displays results in a clean, colorful table with a real-time progress bar.

Service & Banner Grabbing: Identifies common services and attempts to grab service banners for version identification.

Flexible CLI: Easy-to-use command-line arguments for specifying target, port range, timeout, and worker threads.

Installation & Setup

Clone the repository (or download the files):

# This is a hypothetical step for a real Git repo
git clone [https://github.com/999Cypher/port-scanner.git](https://github.com/999Cypher/port-scanner.git)
cd port-scanner


Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


Install the required dependencies:

pip install -r requirements.txt


Usage Examples

The script is easy to run from the command line.

1. Basic Scan (localhost):
To test the scanner on your own machine, scanning the first 100 ports with 50 workers:

python port_scanner.py 127.0.0.1 -p 1-100 -w 50


2. Scan a Target on Your Network:
To scan a specific device (like your laptop) on your home network for all well-known ports (1-1024) with 100 workers:

python port_scanner.py 192.168.1.10 -p 1-1024 -w 100


3. Scan a Specific Port Range:
To check only for common web ports on a target:

python port_scanner.py example.com --ports 80-88,443,8000-8080 --workers 200


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

