"""Unit tests for the check modules."""

import pytest
import subprocess
import socket
import psutil
from collections import namedtuple

# Import the functions to be tested
from checks import cpu, memory, disk, process, network, services

# --- Test for cpu.py ---
def test_check_cpu_usage(mocker):
    """Tests the CPU check function."""
    # Mock psutil.cpu_percent to return a predictable value
    mocker.patch('psutil.cpu_percent', return_value=55.5)
    result = cpu.check_cpu_usage()
    assert result['cpu_percent'] == 55.5

# --- Test for memory.py ---
def test_check_memory_usage(mocker):
    """Tests the memory check function."""
    # Create a mock memory object
    mock_memory = namedtuple('virtual_memory', ['total', 'available', 'percent', 'used', 'free'])
    mock_memory_value = mock_memory(total=1000, available=400, percent=60.0, used=600, free=400)
    mocker.patch('psutil.virtual_memory', return_value=mock_memory_value)
    
    result = memory.check_memory_usage()
    assert result['percent'] == 60.0
    assert result['total'] == 1000

# --- Tests for disk.py ---
def test_check_disk_usage(mocker):
    """Tests the disk check function."""
    # Mock disk_partitions and disk_usage
    mock_partition = namedtuple('sdiskpart', ['device', 'mountpoint'])
    mock_usage = namedtuple('sdiskusage', ['total', 'used', 'free', 'percent'])
    
    mocker.patch('psutil.disk_partitions', return_value=[mock_partition(device='/dev/sda1', mountpoint='/')])
    mocker.patch('psutil.disk_usage', return_value=mock_usage(total=1000, used=850, free=150, percent=85.0))
    
    result = disk.check_disk_usage(threshold=80)
    assert len(result) == 1
    assert result[0]['percent'] == 85.0
    assert result[0]['is_over_threshold'] is True

def test_check_disk_usage_below_threshold(mocker):
    """Tests the disk check when usage is below the threshold."""
    mock_partition = namedtuple('sdiskpart', ['device', 'mountpoint'])
    mock_usage = namedtuple('sdiskusage', ['total', 'used', 'free', 'percent'])
    
    mocker.patch('psutil.disk_partitions', return_value=[mock_partition(device='/dev/sda1', mountpoint='/')])
    mocker.patch('psutil.disk_usage', return_value=mock_usage(total=1000, used=700, free=300, percent=70.0))
    
    result = disk.check_disk_usage(threshold=80)
    assert result[0]['is_over_threshold'] is False

# --- Tests for process.py ---
def test_check_process_running_found(mocker):
    """Tests when the process is found."""
    mock_process = mocker.Mock()
    mock_process.info = {'name': 'test_process'}
    mocker.patch('psutil.process_iter', return_value=[mock_process])
    
    result = process.check_process_running('test_process')
    assert result['status'] == 'running'

def test_check_process_running_not_found(mocker):
    """Tests when the process is not found."""
    mocker.patch('psutil.process_iter', return_value=[])
    result = process.check_process_running('test_process')
    assert result['status'] == 'not_found'

# --- Tests for network.py ---
def test_ping_host_success(mocker):
    """Tests a successful ping."""
    mocker.patch('subprocess.check_output', return_value=b'success')
    assert network.ping_host('8.8.8.8') is True

def test_ping_host_failure(mocker):
    """Tests a failed ping."""
    mocker.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'cmd'))
    assert network.ping_host('8.8.8.8') is False

def test_check_port_open(mocker):
    """Tests an open port."""
    mock_socket = mocker.patch('socket.create_connection')
    assert network.check_port('google.com', 443) is True

def test_check_port_closed(mocker):
    """Tests a closed port."""
    mocker.patch('socket.create_connection', side_effect=socket.error)
    assert network.check_port('google.com', 12345) is False

# --- Tests for services.py ---
def test_get_service_status_windows(mocker):
    """Tests service check on Windows."""
    mock_service = mocker.Mock()
    mock_service.status.return_value = 'running'
    mocker.patch('psutil.win_service_get', return_value=mock_service)
    
    # We need to make sure the NoSuchProcess fallback isn't triggered
    mocker.patch('psutil.process_iter', side_effect=psutil.NoSuchProcess(pid=None, name=None))

    status = services.get_service_status('test_service')
    assert status == 'running'
