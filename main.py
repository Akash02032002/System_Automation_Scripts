import json
import datetime
import argparse

# --- Third-party Libraries ---
# rich is used for creating beautiful, formatted output in the terminal.
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# --- Local Modules ---
# Import the check functions from the 'checks' package.
from checks import cpu, memory, disk, process, network, services

def load_config():
    """
    Loads the configuration from the 'config.json' file.
    This allows for easy modification of check parameters without changing the code.
    """
    with open('config.json', 'r') as f:
        return json.load(f)

def get_all_results(config):
    """
    Gathers results from all check modules by calling their respective functions.
    This function acts as a central point for data collection.
    
    Args:
        config (dict): The configuration dictionary loaded from config.json.

    Returns:
        dict: A dictionary containing the results from all checks.
    """
    return {
        "cpu": cpu.check_cpu_usage(),
        "memory": memory.check_memory_usage(),
        "disk": disk.check_disk_usage(config['disk_check']['threshold_percent']),
        "process": process.check_process_running(config['process_check']['process_name']),
        "network": network.run_network_checks(config['network_check']['hosts_to_ping'], config['network_check']['ports_to_check']),
        "services": services.run_service_checks(config['service_check']['services_to_check'])
    }

def main():
    """
    Main function to run and display system health checks.
    It handles argument parsing, running checks, and displaying the output.
    """
    # --- Argument Parsing ---
    # argparse is used to handle command-line arguments, like --json.
    parser = argparse.ArgumentParser(description="System Health Monitoring Tool.")
    parser.add_argument("--json", help="Export report to a JSON file.", metavar="FILENAME")
    args = parser.parse_args()

    # Initialize the rich console for beautiful output.
    console = Console()
    config = load_config()

    # Show a status message while checks are running.
    with console.status("[bold green]Running health checks...[/]"):
        all_results = get_all_results(config)

    # --- JSON Export ---
    # If the --json argument is provided, dump the results to a file and exit.
    if args.json:
        with open(args.json, 'w') as f:
            # Use indent=4 for pretty-printing the JSON.
            json.dump(all_results, f, indent=4)
        console.print(f"[bold green]Report successfully exported to {args.json}[/]")
        return

    # --- Display Results in Terminal ---
    console.print(Panel(f"[bold cyan]System Health Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold cyan]", expand=False, border_style="blue"))

    # --- System Table --- 
    table = Table(title="System Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("CPU Usage", f"{all_results['cpu']['cpu_percent']:.2f}%")
    table.add_row("Memory Usage", f"{all_results['memory']['percent']:.2f}%")
    table.add_row(f"Process '{all_results['process']['process_name']}'", all_results['process']['status'])
    console.print(table)

    # --- Disk Usage Table ---
    table = Table(title="Disk Usage")
    table.add_column("Mountpoint", style="cyan")
    table.add_column("Usage", style="magenta")
    for d in all_results['disk']:
        # Use color to highlight disks that are over the configured threshold.
        color = "red" if d['is_over_threshold'] else "green"
        table.add_row(d['mountpoint'], f"[{color}]{d['percent']:.2f}%[/{color}]")
    console.print(table)

    # --- Service Status Table ---
    table = Table(title="Service Status")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="magenta")
    for service, status in all_results['services'].items():
        # Use color to indicate service status.
        color = "green" if status == "running" else "red"
        table.add_row(service, f"[{color}]{status}[/{color}]")
    console.print(table)

    # --- Network Checks Table ---
    table = Table(title="Network Checks")
    table.add_column("Check", style="cyan")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="yellow")
    for host, status in all_results['network']['ping_results'].items():
        table.add_row("Ping", host, "[green]Success[/]" if status else "[red]Failed[/]")
    for host, ports in all_results['network']['port_results'].items():
        for port, status in ports.items():
            table.add_row(f"Port Check", f"{host}:{port}", "[green]Open[/]" if status else "[red]Closed[/]")
    console.print(table)

# Standard Python entry point.
if __name__ == "__main__":
    main()
