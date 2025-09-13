"""Performs CPU-related checks."""

import psutil

def check_cpu_usage():
    """
    Checks the current system-wide CPU utilization.

    Returns:
        dict: A dictionary containing the CPU usage percentage.
    """
    # psutil.cpu_percent(interval=1) gets the usage over a 1-second interval.
    # This is more accurate than a non-blocking call.
    return {
        "cpu_percent": psutil.cpu_percent(interval=1)
    }
