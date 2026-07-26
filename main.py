#!/usr/bin/env python3
"""
Android Repair CLI - Main Entry Point
Complete CLI tool for Android device recovery, FRP fix, and system repair
"""

import click
import logging
import sys
import os
from pathlib import Path
from colorama import Fore, Style, init
from datetime import datetime

# Import custom modules
try:
    from adb_manager import ADBManager
    from device_detector import DeviceDetector
    from frp_fixer import FRPFixer
    from recovery_manager import RecoveryManager
except ImportError:
    print(f"{Fore.RED}Error: Required modules not found. Please run: pip install -r requirements.txt{Style.RESET_ALL}")
    sys.exit(1)

init(autoreset=True)

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"android_repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize managers
adb_manager = ADBManager()
device_detector = DeviceDetector()
frp_fixer = FRPFixer(adb_manager)
recovery_manager = RecoveryManager(adb_manager)


@click.group()
def cli():
    """Android Repair CLI - Device Recovery & FRP Fix Tool"""
    pass


@cli.command()
def version():
    """Show version information"""
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW}Android Repair CLI v1.0.0{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}  Device Recovery & FRP Fix Tool")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}  Author: Cherish594")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}  Repository: github.com/Cherish594/www.cherishedcclxv.com")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")


@cli.command()
def check_adb():
    """Check ADB connection status"""
    print(f"{Fore.YELLOW}[*] Checking ADB connection...{Style.RESET_ALL}")
    
    if adb_manager.check_adb_connection():
        print(f"{Fore.GREEN}[+] ADB is available and running{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] ADB is not available. Please install Android SDK Platform Tools{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[!] Download from: https://developer.android.com/tools/adb{Style.RESET_ALL}")


@cli.command()
def devices():
    """List all connected devices"""
    print(f"{Fore.YELLOW}[*] Scanning for connected devices...{Style.RESET_ALL}")
    
    connected = adb_manager.get_connected_devices()
    
    if not connected:
        print(f"{Fore.YELLOW}[!] No devices connected{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[!] Make sure:")
        print(f"    1. Device is connected via USB")
        print(f"    2. USB debugging is enabled on device")
        print(f"    3. You authorized the connection{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}[+] Found {len(connected)} device(s):{Style.RESET_ALL}")
    for i, device in enumerate(connected, 1):
        print(f"{Fore.CYAN}  {i}. {device}{Style.RESET_ALL}")


@cli.command()
@click.argument('device_id', required=False)
def info(device_id):
    """Get detailed device information"""
    if not device_id:
        devices_list = adb_manager.get_connected_devices()
        if not devices_list:
            print(f"{Fore.RED}[-] No devices connected{Style.RESET_ALL}")
            return
        device_id = devices_list[0]
        print(f"{Fore.YELLOW}[*] Using device: {device_id}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}[*] Reading device information...{Style.RESET_ALL}")
    
    props = adb_manager.get_device_info(device_id)
    print(device_detector.format_device_info(props))
    
    # Battery info
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Battery Information{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    battery = adb_manager.get_battery_info(device_id)
    for key, value in battery.items():
        if key.strip():
            print(f"{Fore.GREEN}{key}{Style.RESET_ALL}: {value}")
    
    # Root status
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Root Status{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    root_status = adb_manager.get_root_status(device_id)
    for check, status in root_status.items():
        status_text = f"{Fore.GREEN}YES{Style.RESET_ALL}" if status else f"{Fore.RED}NO{Style.RESET_ALL}"
        print(f"{Fore.GREEN}{check}{Style.RESET_ALL}: {status_text}")


@cli.command()
@click.argument('device_id', required=False)
@click.option('--method', default='adb_removal', help='FRP removal method')
def fix_frp(device_id, method):
    """Fix FRP (Factory Reset Protection)"""
    if not device_id:
        devices_list = adb_manager.get_connected_devices()
        if not devices_list:
            print(f"{Fore.RED}[-] No devices connected{Style.RESET_ALL}")
            return
        device_id = devices_list[0]
    
    print(f"{Fore.YELLOW}[*] Device: {device_id}{Style.RESET_ALL}")
    
    # Check FRP status
    frp_status = frp_fixer.get_frp_status(device_id)
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}FRP Status Check{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if frp_status["is_locked"]:
        print(f"{Fore.RED}[!] Device is FRP locked{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[+] Device appears to be FRP unlocked{Style.RESET_ALL}")
    
    if frp_status["google_accounts"]:
        print(f"{Fore.YELLOW}[!] Google accounts detected:{Style.RESET_ALL}")
        for acc in frp_status["google_accounts"]:
            print(f"    - {acc}")
    
    # Perform FRP fix
    print(f"\n{Fore.CYAN}Attempting FRP fix with method: {method}{Style.RESET_ALL}")
    success, message = frp_fixer.perform_frp_fix(device_id, method)
    
    if success:
        print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")


@cli.command()
@click.argument('device_id', required=False)
@click.option('--confirm', is_flag=True, help='Confirm factory reset')
def factory_reset(device_id, confirm):
    """Perform factory reset"""
    if not device_id:
        devices_list = adb_manager.get_connected_devices()
        if not devices_list:
            print(f"{Fore.RED}[-] No devices connected{Style.RESET_ALL}")
            return
        device_id = devices_list[0]
    
    if not confirm:
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] WARNING: Factory reset will erase ALL data!{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}To confirm, run: android-repair factory-reset {device_id} --confirm{Style.RESET_ALL}")
        return
    
    success, message = recovery_manager.factory_reset(device_id, confirm=True)
    if success:
        print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}")


@cli.command()
@click.argument('device_id', required=False)
def wipe_cache(device_id):
    """Wipe device cache"""
    if not device_id:
        devices_list = adb_manager.get_connected_devices()
        if not devices_list:
            print(f"{Fore.RED}[-] No devices connected{Style.RESET_ALL}")
            return
        device_id = devices_list[0]
    
    success, message = recovery_manager.wipe_cache(device_id)
    if success:
        print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}")


@cli.command()
@click.argument('device_id', required=False)
@click.option('--path', default='backups', help='Backup destination path')
def backup(device_id, path):
    """Backup device data"""
    if not device_id:
        devices_list = adb_manager.get_connected_devices()
        if not devices_list:
            print(f"{Fore.RED}[-] No devices connected{Style.RESET_ALL}")
            return
        device_id = devices_list[0]
    
    success, message = recovery_manager.backup_device(device_id, path)
    if success:
        print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}")


@cli.command()
def help_guide():
    """Show help and usage guide"""
    guide = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}           {Fore.YELLOW}Android Repair CLI - Usage Guide{Style.RESET_ALL}
{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}QUICK START:{Style.RESET_ALL}
  1. Connect your device via USB
  2. Enable USB debugging on device
  3. Run commands below

{Fore.GREEN}BASIC COMMANDS:{Style.RESET_ALL}

  {Fore.YELLOW}android-repair check-adb{Style.RESET_ALL}
    → Check if ADB is working

  {Fore.YELLOW}android-repair devices{Style.RESET_ALL}
    → List all connected devices

  {Fore.YELLOW}android-repair info{Style.RESET_ALL}
    → Get detailed device information

{Fore.GREEN}RECOVERY & FRP COMMANDS:{Style.RESET_ALL}

  {Fore.YELLOW}android-repair fix-frp{Style.RESET_ALL}
    → Fix FRP lock on device

  {Fore.YELLOW}android-repair factory-reset --confirm{Style.RESET_ALL}
    → Perform factory reset (WARNING: erases all data)

  {Fore.YELLOW}android-repair wipe-cache{Style.RESET_ALL}
    → Wipe device cache

  {Fore.YELLOW}android-repair backup{Style.RESET_ALL}
    → Backup device data before recovery

{Fore.GREEN}DEVICE SETUP:{Style.RESET_ALL}

  1. Connect device via USB cable
  2. Go to Settings → About Phone
  3. Tap "Build Number" 7 times
  4. Go to Settings → Developer Options
  5. Enable "USB Debugging"
  6. Authorize the computer connection

{Fore.GREEN}SUPPORTED DEVICES:{Style.RESET_ALL}
  • Tecno Spark Go (KL4)
  • Samsung Galaxy A/S series
  • Xiaomi Redmi series
  • And many more Android devices

{Fore.RED}⚠️  DISCLAIMER:{Style.RESET_ALL}
  Use at your own risk! This tool modifies device settings.
  Always backup your data before proceeding.

{Fore.CYAN}For more info: github.com/Cherish594/www.cherishedcclxv.com{Style.RESET_ALL}
    """
    print(guide)


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
        logger.exception("An error occurred")
        sys.exit(1)
