"""Performs system service-related checks."""

import psutil

def get_service_status(service_name):
    """
    Gets the status of a specific system service.

    This function has platform-specific behavior:
    - On Windows, it uses psutil's dedicated win_service_get to get detailed status.
    - On other systems (like Linux), it performs a simplified check by looking for a 
      running process with a matching name, as there is no universal cross-platform
      API for services in psutil.

    Args:
        service_name (str): The name of the service to check.

    Returns:
        str: The status of the service (e.g., 'running', 'stopped', 'not_found').
    """
    try:
        # This is the primary method for Windows services.
        service = psutil.win_service_get(service_name)
        return service.status()
    except psutil.NoSuchProcess:
        # This exception can be raised on non-Windows systems or if the service doesn't exist.
        # Fallback for Linux/macOS: check if a process with the same name is running.
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == service_name:
                return "running" # Simplified status
        return "not_found"
    except Exception:
        # Catch any other exceptions (e.g., permission errors) and return a generic error.
        return "error"

def run_service_checks(services_to_check):
    """
    Runs all configured service checks.

    Args:
        services_to_check (list): A list of service names to check.

    Returns:
        dict: A dictionary mapping service names to their status.
    """
    return {service: get_service_status(service) for service in services_to_check}
