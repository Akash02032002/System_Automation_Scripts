"""Performs network-related checks, such as pinging hosts and checking ports."""

import socket
import subprocess
import platform

def ping_host(host):
    """
    Pings a host to check for connectivity.

    Args:
        host (str): The hostname or IP address to ping.

    Returns:
        bool: True if the ping is successful, False otherwise.
    """
    # The ping command is different on Windows vs. Linux/macOS.
    # -n 1 on Windows, -c 1 on others, to send just one packet.
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    
    try:
        # Run the command and hide the output.
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If the command fails (host unreachable) or isn't found, return False.
        return False

def check_port(host, port):
    """
    Checks if a specific TCP port is open on a host.

    Args:
        host (str): The hostname or IP address to check.
        port (int): The port number to check.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    try:
        # Try to create a connection to the host and port.
        # The `with` statement ensures the socket is closed automatically.
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.error, socket.timeout):
        # If the connection fails or times out, the port is likely closed.
        return False

def run_network_checks(hosts_to_ping, ports_to_check):
    """
    Runs all configured network checks.

    Args:
        hosts_to_ping (list): A list of hosts to ping.
        ports_to_check (dict): A dictionary of hosts and the ports to check on them.

    Returns:
        dict: A dictionary containing the results of the ping and port checks.
    """
    ping_results = {host: ping_host(host) for host in hosts_to_ping}
    
    port_results = {}
    for host, ports in ports_to_check.items():
        port_results[host] = {port: check_port(host, port) for port in ports}
        
    return {
        "ping_results": ping_results,
        "port_results": port_results
    }
