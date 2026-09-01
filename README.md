# windows-service-watchdog-powershell
Infrastructure auto-restart resilience, background process monitoring, and self-healing server script execution

# Windows Service Watchdog

A lightweight, automated service monitoring and recovery engine designed to keep critical Windows services running. Built with Python (`pywin32`) and packaged with PowerShell automation scripts for enterprise server deployment.

## Features

* **Automated Service Recovery:** Periodically checks target Windows services (`AQIS.Service`, `AquariusEventProcessor`, `AquariusAnalyticsRecorder`) and issues start commands automatically if a service is stopped or faulted.
* **Dual Execution Modes:** Supports continuous loop monitoring (`--interval`) or single-shot execution (`--once`) optimized for Windows Task Scheduler.
* **Log Rotation:** Uses rotating log files (`5MB` cap, `5` backups) to prevent log directory storage bloat.
* **PowerShell Automation:** Includes deployment scripts to quickly register or unregister the watchdog as an elevated `NT AUTHORITY\SYSTEM` Scheduled Task.

---

## Directory Structure

```text
windows-service-watchdog-powershell/
├── .github/
│   └── workflows/
│       └── lint_and_test.yml       # Syntax validation on push
├── src/
│   ├── __init__.py
│   └── service_watchdog.py         # Core Python monitoring engine
├── scripts/
│   ├── Install-WatchdogTask.ps1    # Task Scheduler installation script
│   └── Uninstall-WatchdogTask.ps1  # Cleanup script
├── tests/
│   └── test_watchdog.py            # Unit tests
├── .gitignore
├── README.md
└── requirements.txt

```

---

## Prerequisites & Installation

* **Operating System:** Windows Server / Windows 10+
* **Permissions:** Administrator privileges (required to query and control Windows Services)
* **Environment:** Python 3.10+

### Setup

1. Clone the repository to the target Windows machine:
```cmd
git clone [https://github.com/your-username/windows-service-watchdog-powershell.git](https://github.com/your-username/windows-service-watchdog-powershell.git)
cd windows-service-watchdog-powershell

```


2. Install requirements:
```cmd
pip install -r requirements.txt

```



---

## Usage

### Running via Python Command Line

**Run once (Single Status Check):**

```cmd
python src\service_watchdog.py --once

```

**Run continuously (Interval Mode):**

```cmd
python src\service_watchdog.py --interval 300

```

* **Custom Log Directory:** Override default log paths by setting the `WATCHDOG_LOG_DIR` environment variable before execution:
```cmd
set WATCHDOG_LOG_DIR=C:\Logs\Watchdog
python src\service_watchdog.py --once

```



---

## Deploying as a Windows Scheduled Task

To deploy this script as an automated background system task running every 5 minutes:

1. Open **PowerShell as Administrator**.
2. Run the deployment script:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\scripts\Install-WatchdogTask.ps1

```



To remove the scheduled task:

```powershell
.\scripts\Uninstall-WatchdogTask.ps1

```

---

## Logging

Logs are saved locally to `C:\Converter\Magat\debug\aquariusservicewatcher.log` by default.

**Sample Log Output:**

```text
2026-09-01 18:00:00 [INFO] Aquarius Service Watcher initialized.
2026-09-01 18:00:01 [WARNING] Service 'AQIS.Service' is not RUNNING (state=1). Attempting start.
2026-09-01 18:00:02 [INFO] Start command issued for service 'AQIS.Service'
2026-09-01 18:05:00 [INFO] All monitored services are RUNNING.

```

---

## License

MIT License. Free for internal deployment and modification.

```

```
