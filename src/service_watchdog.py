import os
import sys
import time
import logging
import argparse
from logging.handlers import RotatingFileHandler

# Target Windows Services
MONITORED_SERVICES = [
    "AQIS.Service",
    "AquariusEventProcessor",
    "AquariusAnalyticsRecorder"
]

# Configuration via Environment Variables with Fallbacks
DEFAULT_LOG_DIR = os.getenv("WATCHDOG_LOG_DIR", r"C:\Converter\Magat\debug")
LOG_FILE = "aquariusservicewatcher.log"
LOG_PATH = os.path.join(DEFAULT_LOG_DIR, LOG_FILE)

MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5

def setup_logger():
    os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
    logger = logging.getLogger("AquariusServiceWatcher")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = RotatingFileHandler(
            LOG_PATH, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT, encoding="utf-8"
        )
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

def ensure_service_running(service_name, logger):
    if sys.platform != "win32":
        logger.error("win32service is only supported on Windows operating systems.")
        return False

    import win32service
    import win32serviceutil

    try:
        status = win32serviceutil.QueryServiceStatus(service_name)[1]

        if status == win32service.SERVICE_RUNNING:
            return True

        logger.warning(f"Service '{service_name}' is not RUNNING (state={status}). Attempting start.")
        win32serviceutil.StartService(service_name)
        logger.info(f"Start command issued for service '{service_name}'")
        return False

    except Exception as e:
        logger.error(f"Failed to check/start service '{service_name}': {e}")
        return False

def check_services(logger):
    all_running = True
    for service in MONITORED_SERVICES:
        if not ensure_service_running(service, logger):
            all_running = False

    if all_running:
        logger.info("All monitored services are RUNNING.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Windows Service Watchdog Engine")
    parser.add_argument("--once", action="store_true", help="Run a single status check and exit (ideal for Task Scheduler)")
    parser.add_argument("--interval", type=int, default=300, help="Loop interval in seconds (default: 300)")
    args = parser.parse_args()

    log = setup_logger()
    log.info("Aquarius Service Watcher initialized.")

    if args.once:
        check_services(log)
    else:
        try:
            while True:
                check_services(log)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            log.info("Service Watcher stopped manually.")
        except Exception as err:
            log.exception(f"Fatal watchdog error: {err}")
