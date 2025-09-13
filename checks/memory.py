"""Performs memory-related checks."""

import psutil

def check_memory_usage():
    """
    Checks the system's virtual memory usage.

    Returns:
        dict: A dictionary containing detailed memory statistics.
    """
    # psutil.virtual_memory() returns a named tuple with memory statistics.
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent,
        "used": memory.used,
        "free": memory.free
    }
