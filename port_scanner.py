import socket
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import time
# --- NEW IMPORT for concurrency ---
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize rich console for beautiful output
console = Console()

def get_banner(s):
    """
    Attempts to grab the banner (service version) from an open port.
    Returns the banner string or an empty string if it fails.
    """
    try:
        # Some services send a banner immediately upon connection
        banner = s.recv(1024).decode(errors='ignore').strip()
        return banner
    except Exception:
        return ""

def scan_port(ip, port, timeout):
    """
    Scans a single port on the given IP address.
    Returns a tuple: (port, is_open, banner)
    """
    try:
        # Create a new socket for each port scan
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            # Use connect_ex to avoid exceptions for closed ports
            if s.connect_ex((ip, port)) == 0:
                banner = get_banner(s)
                # Return the port number along with the result
                return port, True, banner
    except socket.error as e:
        # This might happen if the hostname is invalid, etc.
        # We'll print errors at the end to keep the progress bar clean
        pass
    
    # Return port number even on failure
    return port, False, ""


def main():
    """
    Main function to parse arguments and run the scanner.
    """
    # Create an argument parser object
    parser = argparse.ArgumentParser(
        description="A cool and fast Python port scanner with a rich UI.",
        epilog="Example: python port_scanner.py 127.0.0.1 -p 1-100 -w 50"
    )

    # Add arguments
    parser.add_argument("target", help="The IP address or hostname to scan.")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range to scan (e.g., '22-8080').")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Connection timeout in seconds for each port.")
    # --- NEW ARGUMENT for concurrency ---
    parser.add_argument("-w", "--workers", type=int, default=100, help="Number of concurrent threads (workers) to use.")

    # Parse the arguments provided by the user
    args = parser.parse_args()

    target_ip = args.target
    port_range_str = args.ports
    timeout = args.timeout
    num_workers = args.workers

    # --- Script's main logic ---
    console.print(f"\n[bold cyan]Scanning target:[/] [bright_magenta]{target_ip}[/bright_magenta]")
    console.print(f"[bold cyan]Port range:[/] [bright_magenta]{port_range_str}[/bright_magenta]")
    console.print(f"[bold cyan]Worker threads:[/] [bright_magenta]{num_workers}[/bright_magenta]\n")

    try:
        # Parse the port range (e.g., '1-1024')
        start_port, end_port = map(int, port_range_str.split('-'))
        ports_to_scan = range(start_port, end_port + 1)
        total_ports = len(ports_to_scan)
    except ValueError:
        console.print("[bold red]Error: Invalid port range format. Please use 'start-end'.[/bold red]")
        return

    open_ports_data = []

    # --- CONCURRENT SCANNING LOGIC ---
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Scanning ports...", total=total_ports)
        
        # Use ThreadPoolExecutor to manage a pool of worker threads
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Submit all scan_port tasks to the executor
            # This creates a "future" object for each task
            future_to_port = {executor.submit(scan_port, target_ip, port, timeout): port for port in ports_to_scan}
            
            # Process results as they are completed
            for future in as_completed(future_to_port):
                port, is_open, banner = future.result()
                
                if is_open:
                    try:
                        service = socket.getservbyport(port, 'tcp')
                    except OSError:
                        service = "Unknown"
                    open_ports_data.append((port, service, banner))
                
                # Update the progress bar for each completed task
                progress.update(task, advance=1)

    # Sort the results by port number for clean output
    open_ports_data.sort(key=lambda x: x[0])

    # --- Display results in a beautiful table using rich ---
    if open_ports_data:
        table = Table(title=f"Open Ports on {target_ip}", show_header=True, header_style="bold magenta")
        table.add_column("Port", justify="right", style="dim", width=12)
        table.add_column("Service", style="cyan")
        table.add_column("Banner", style="green")

        for port, service, banner in open_ports_data:
            table.add_row(str(port), service, banner)

        console.print(table)
    else:
        console.print(f"\n[bold yellow]No open ports found in the range {port_range_str} on {target_ip}.[/bold yellow]")

if __name__ == "__main__":
    main()

