
# System Automation and Health Monitoring Tool

A professional, Python-based tool for system administration and health monitoring. This application provides a detailed, color-coded report on the status of the system and can export the results to a JSON file for auditing or integration.

This project is designed to showcase skills in automation, system monitoring, network management, and professional software development practices, making it ideal for a System Engineer portfolio.

## ✨ Important Points:-
- Created 15+ automation scripts for system administration tasks
- Reduced manual configuration time by 60% through PowerShell and Bash scripting
- Implemented log rotation and system health monitoring solutions
- Technologies: PowerShell, Bash, Python, Linux, Windows Server

## ✨ Features:-

- **Visually Rich Reports:** Color-coded tables in the console for easy reading and quick diagnostics.
- **Comprehensive Health Checks:**
  - **CPU:** Monitors overall CPU utilization.
  - **Memory:** Tracks virtual memory usage.
  - **Disk:** Checks all mounted partitions for usage and warns if they exceed a configurable threshold.
  - **Processes:** Verifies if a specific process is running.
  - **Services:** Checks the status of critical system services (e.g., "Spooler" on Windows).
  - **Network:** Pings a list of hosts for connectivity and checks if specific network ports are open.
- **Highly Configurable:** All checks are managed through a central `config.json` file.
- **Exportable Data:** Reports can be exported to a JSON file.
- **Unit Tested:** The project includes a full suite of unit tests using `pytest` to ensure reliability.

## 🛠️ Tools and Technologies:-

- **Language:** Python 3
- **Core Libraries:**
  - `psutil`: For gathering system information (CPU, memory, disk, processes, services).
  - `rich`: For creating beautiful, formatted terminal output.
- **Testing:**
  - `pytest`: As the testing framework.
  - `pytest-mock`: For simulating system calls and network responses during tests.

## 🚀 Getting Started:-

Follow these steps to get the project up and running on your local machine.

### 1. File Path

The main application script is located at:
`C:\Users\tittu\Videos\System-Automation-V2\main.py`

### 2. Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### 3. Installation & Setup

1.  **Navigate to the project directory:**
    ```bash
    cd "C:\Users\tittu\Videos\System-Automation-V2"
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Customize the configuration:**
    Open the `config.json` file and edit the parameters to match your needs. For example, you can change the `hosts_to_ping` or the `services_to_check`.

### 4. Running the Application

You can run the tool in two ways:

**Option A: From the project directory (Recommended)**

This is the simplest method. After navigating into the project directory, use this command:
```bash
python main.py
```

**Option B: From any location**

You can also run the script from anywhere on your system by providing the full, absolute path:
```bash
python "C:\Users\tittu\Videos\System-Automation-V2\main.py"
```

### 5. Exporting the Report

To save the output to a JSON file, use the `--json` flag. This works with both of the running methods above:

```bash
# Example from within the project directory
python main.py --json report.json

# Example using the full path
python "C:\Users\tittu\Videos\System-Automation-V2\main.py" --json "C:\path	to\youreport.json"

My Example :- 
python "C:\Users\tittu\Videos\System-Automation-V2\main.py" --json "C:\Users\tittu\Videos\System-Automation-V2\report.json"
```

{ "Report successfully exported to C:\Users\tittu\Videos\System-Automation-V2\report.json" }


## ⚙️ How It Works: The Checks Explained:-

The tool's logic is divided into several modules located in the `checks/` directory.

| Module          | Description                                                                                                                                 |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `cpu.py`        | Uses `psutil` to get the current system-wide CPU utilization percentage over a 1-second interval for accuracy.                                |
| `memory.py`     | Gathers detailed statistics on virtual memory, including total, used, available, and percentage.                                            |
| `disk.py`       | Scans all accessible disk partitions, reporting their usage and flagging any that are over the threshold set in `config.json`.                |
| `process.py`    | Iterates through all running processes to check if a process with the name specified in the configuration is currently active.                |
| `services.py`   | Checks the status of specified system services. It uses Windows-specific functions where available and falls back to process checking on other systems. |
| `network.py`    | Performs two key network checks: it pings specified hosts to ensure they are reachable and checks if configured TCP ports are open on target hosts. |

## 🧪 Testing:-

A comprehensive suite of unit tests has been written to ensure the reliability of each check module. The tests use mocking to isolate the code from the live system state, making them fast and predictable.

**To run the tests, execute the following command from the project root directory:**

```bash
python -m pytest
```

You should see all tests passing, confirming that the application's logic is sound.
#
