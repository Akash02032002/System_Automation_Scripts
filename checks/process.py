"""Performs process-related checks."""

import psutil

def check_process_running(process_name):
    """
    Checks if a process with a specific name is currently running.

    Args:
        process_name (str): The name of the process to look for.

    Returns:
        dict: A dictionary containing the process name and its status ('running' or 'not_found').
    """
    # Iterate over all running processes.
    for proc in psutil.process_iter(['name']):
        # Check if the process name matches the one we're looking for.
        if proc.info['name'] == process_name:
            return { "process_name": process_name, "status": "running" }
    
    # If the loop completes without finding the process, it's not running.
    return { "process_name": process_name, "status": "not_found" }
