"""Performs disk-related checks."""

import psutil

def check_disk_usage(threshold):
    """
    Checks the usage of all mounted disk partitions.

    Args:
        threshold (int): The usage percentage above which a warning should be triggered.

    Returns:
        list: A list of dictionaries, where each dictionary contains details for a partition.
    """
    partitions = psutil.disk_partitions()
    results = []
    for p in partitions:
        try:
            # Get usage statistics for the partition's mount point.
            usage = psutil.disk_usage(p.mountpoint)
            is_over_threshold = usage.percent > threshold
            results.append({
                "device": p.device,
                "mountpoint": p.mountpoint,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
                "is_over_threshold": is_over_threshold
            })
        except PermissionError:
            # Some devices (like CD-ROMs) might not be accessible.
            # We just skip them and continue.
            continue
    return results
