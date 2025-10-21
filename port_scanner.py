#!/usr/bin/env python3
"""
Port Scanner with Rich Terminal UI
A Python tool for scanning and identifying open ports on target hosts.
"""

import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Tuple

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
except ImportError:
    print("Error: 'rich' library not found. Please install it using: pip install rich")
    sys.exit(1)

console = Console()


def scan_port(host: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str]:
    """
    Scan a single port on the target host.
    
    Args:
        host: Target hostname or IP address
        port: Port number to scan
        timeout: Connection timeout in seconds
        
    Returns:
        Tuple of (port, is_open, service_name)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            return (port, True, service)
        else:
            return (port, False, "")
    except socket.gaierror:
        return (port, False, "")
    except socket.error:
        return (port, False, "")


def parse_port_range(port_range: str) -> List[int]:
    """
    Parse port range string into list of ports.
    
    Args:
        port_range: Port range string (e.g., "80", "1-100", "22,80,443")
        
    Returns:
        List of port numbers
    """
    ports = []
    
    # Handle comma-separated ports
    parts = port_range.split(',')
    
    for part in parts:
        part = part.strip()
        # Handle range (e.g., "1-100")
        if '-' in part:
            start, end = part.split('-')
            try:
                start = int(start.strip())
                end = int(end.strip())
                if start <= end and 1 <= start <= 65535 and 1 <= end <= 65535:
                    ports.extend(range(start, end + 1))
                else:
                    console.print(f"[red]Invalid port range: {part}[/red]")
            except ValueError:
                console.print(f"[red]Invalid port range: {part}[/red]")
        else:
            # Single port
            try:
                port = int(part)
                if 1 <= port <= 65535:
                    ports.append(port)
                else:
                    console.print(f"[red]Invalid port number: {port}[/red]")
            except ValueError:
                console.print(f"[red]Invalid port number: {part}[/red]")
    
    return sorted(list(set(ports)))


def scan_ports(host: str, ports: List[int], timeout: float = 1.0, max_workers: int = 100) -> List[Tuple[int, bool, str]]:
    """
    Scan multiple ports on target host using concurrent threads.
    
    Args:
        host: Target hostname or IP address
        ports: List of port numbers to scan
        timeout: Connection timeout in seconds
        max_workers: Maximum number of concurrent threads
        
    Returns:
        List of tuples (port, is_open, service_name)
    """
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        task = progress.add_task(f"[cyan]Scanning {host}...", total=len(ports))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(scan_port, host, port, timeout): port for port in ports}
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                progress.update(task, advance=1)
    
    return sorted(results, key=lambda x: x[0])


def display_results(host: str, results: List[Tuple[int, bool, str]], start_time: datetime, end_time: datetime):
    """
    Display scan results in a beautiful table format.
    
    Args:
        host: Target hostname or IP address
        results: List of scan results
        start_time: Scan start time
        end_time: Scan end time
    """
    open_ports = [r for r in results if r[1]]
    
    # Display header
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]Port Scan Results for {host}[/bold cyan]",
        border_style="cyan"
    ))
    
    # Display open ports table
    if open_ports:
        table = Table(
            title=f"[green]Found {len(open_ports)} Open Port(s)[/green]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Port", justify="right", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center", style="green")
        table.add_column("Service", justify="left", style="yellow")
        
        for port, is_open, service in open_ports:
            table.add_row(
                str(port),
                "OPEN",
                service
            )
        
        console.print(table)
    else:
        console.print("[yellow]No open ports found in the specified range.[/yellow]")
    
    # Display summary
    duration = (end_time - start_time).total_seconds()
    console.print()
    console.print(Panel.fit(
        f"[bold]Scan Summary[/bold]\n"
        f"Total Ports Scanned: {len(results)}\n"
        f"Open Ports: {len(open_ports)}\n"
        f"Closed Ports: {len(results) - len(open_ports)}\n"
        f"Duration: {duration:.2f} seconds",
        border_style="blue"
    ))
    console.print()


def main():
    """Main function to run the port scanner."""
    parser = argparse.ArgumentParser(
        description="Port Scanner - Scan and identify open ports on target hosts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py 192.168.1.1 -p 80
  python port_scanner.py example.com -p 1-1000
  python port_scanner.py localhost -p 22,80,443,8080
  python port_scanner.py 192.168.1.1 -p 1-65535 -t 0.5 -w 200
        """
    )
    
    parser.add_argument(
        "target",
        help="Target hostname or IP address to scan"
    )
    
    parser.add_argument(
        "-p", "--ports",
        default="1-1024",
        help="Port(s) to scan. Can be a single port (80), range (1-1000), or comma-separated (22,80,443). Default: 1-1024"
    )
    
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=1.0,
        help="Connection timeout in seconds. Default: 1.0"
    )
    
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=100,
        help="Maximum number of concurrent threads. Default: 100"
    )
    
    args = parser.parse_args()
    
    # Display banner
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Port Scanner[/bold cyan]\n"
        "[dim]Scan and identify open ports on target hosts[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    # Parse ports
    ports = parse_port_range(args.ports)
    
    if not ports:
        console.print("[red]Error: No valid ports to scan.[/red]")
        sys.exit(1)
    
    # Resolve hostname
    try:
        target_ip = socket.gethostbyname(args.target)
        console.print(f"[cyan]Target:[/cyan] {args.target} ({target_ip})")
        console.print(f"[cyan]Ports:[/cyan] {len(ports)} port(s)")
        console.print(f"[cyan]Timeout:[/cyan] {args.timeout}s")
        console.print()
    except socket.gaierror:
        console.print(f"[red]Error: Could not resolve hostname '{args.target}'[/red]")
        sys.exit(1)
    
    # Scan ports
    try:
        start_time = datetime.now()
        results = scan_ports(target_ip, ports, args.timeout, args.workers)
        end_time = datetime.now()
        
        # Display results
        display_results(args.target, results, start_time, end_time)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Scan interrupted by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error during scan: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
