import socket
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import time

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
    Returns a tuple: (is_open, banner)
    """
    try:
        # Create a new socket for each port scan
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            # Use connect_ex to avoid exceptions for closed ports
            if s.connect_ex((ip, port)) == 0:
                banner = get_banner(s)
                return True, banner
    except socket.error as e:
        # This might happen if the hostname is invalid, etc.
        console.print(f"[bold red]Socket error: {e}[/bold red]")
    
    return False, ""


def main():
    """
    Main function to parse arguments and run the scanner.
    """
    # --- Step 3: Implement Command-Line Interface ---
    # Create an argument parser object
    parser = argparse.ArgumentParser(
        description="A cool Python port scanner with a rich UI.",
        epilog="Example: python port_scanner.py 127.0.0.1 -p 1-100"
    )

    # Add arguments
    parser.add_argument("target", help="The IP address or hostname to scan.")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range to scan (e.g., '22-8080').")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Connection timeout in seconds for each port.")

    # Parse the arguments provided by the user
    args = parser.parse_args()

    target_ip = args.target
    port_range_str = args.ports
    timeout = args.timeout

    # --- Script's main logic ---
    console.print(f"\n[bold cyan]Scanning target:[/] [bright_magenta]{target_ip}[/bright_magenta]")
    console.print(f"[bold cyan]Port range:[/] [bright_magenta]{port_range_str}[/bright_magenta]\n")

    try:
        # Parse the port range (e.g., '1-1024')
        start_port, end_port = map(int, port_range_str.split('-'))
        total_ports = end_port - start_port + 1
    except ValueError:
        console.print("[bold red]Error: Invalid port range format. Please use 'start-end'.[/bold red]")
        return

    open_ports_data = []

    # --- Step 2: Use rich library for a progress bar ---
    with Progress(console=console) as progress:
        task = progress.add_task("[green]Scanning ports...", total=total_ports)

        for port in range(start_port, end_port + 1):
            is_open, banner = scan_port(target_ip, port, timeout)
            if is_open:
                # Get the service name if it's a well-known port
                try:
                    service = socket.getservbyport(port, 'tcp')
                except OSError:
                    service = "Unknown"
                open_ports_data.append((port, service, banner))

            progress.update(task, advance=1)
            # Give a slight delay to make the progress bar visible for fast scans
            time.sleep(0.01) 

    # --- Display results in a beautiful table using rich ---
    if open_ports_data:
        table = Table(title=f"Open Ports on {target_ip}", show_header=True, header_style="bold magenta")
        table.add_column("Port", style="dim", width=12)
        table.add_column("Service", style="cyan")
        table.add_column("Banner", style="green")

        for port, service, banner in open_ports_data:
            table.add_row(str(port), service, banner)

        console.print(table)
    else:
        console.print(f"\n[bold yellow]No open ports found in the range {port_range_str} on {target_ip}.[/bold yellow]")

if __name__ == "__main__":
    main()
