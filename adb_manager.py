#!/usr/bin/env python3
"""
ADB Manager Module - Handles all ADB connections and commands
"""

import subprocess
import time
import logging
from typing import List, Dict, Tuple, Optional
from colorama import Fore, Style, init

init(autoreset=True)

logger = logging.getLogger(__name__)


class ADBManager:
    """Manages ADB connections and device communication"""

    def __init__(self, adb_path: str = "adb", timeout: int = 30):
        self.adb_path = adb_path
        self.timeout = timeout
        self.connected_devices = []
        self.current_device = None

    def execute_command(self, command: str, device_id: Optional[str] = None) -> Tuple[bool, str]:
        """
        Execute an ADB command
        Args:
            command: The ADB command to execute
            device_id: Specific device ID (optional)
        Returns:
            Tuple of (success, output)
        """
        try:
            if device_id:
                full_command = f"{self.adb_path} -s {device_id} {command}"
            else:
                full_command = f"{self.adb_path} {command}"

            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {self.timeout} seconds"
        except Exception as e:
            return False, str(e)

    def check_adb_connection(self) -> bool:
        """
        Check if ADB is available and running
        Returns:
            True if ADB is available, False otherwise
        """
        success, output = self.execute_command("devices")
        return success

    def get_connected_devices(self) -> List[str]:
        """
        Get list of connected devices
        Returns:
            List of device IDs
        """
        success, output = self.execute_command("devices")
        if not success:
            print(f"{Fore.RED}[ERROR] Failed to get devices: {output}{Style.RESET_ALL}")
            return []

        devices = []
        for line in output.split("\n"):
            if "device" in line and "List" not in line:
                device_id = line.split()[0]
                if device_id:
                    devices.append(device_id)

        self.connected_devices = devices
        return devices

    def get_device_info(self, device_id: str) -> Dict[str, str]:
        """
        Get detailed device information
        Args:
            device_id: Device ID
        Returns:
            Dictionary of device properties
        """
        info = {}
        properties = [
            "ro.build.version.release",
            "ro.build.version.sdk",
            "ro.product.brand",
            "ro.product.model",
            "ro.product.device",
            "ro.serialno",
            "ro.build.fingerprint",
            "ro.build.id",
            "ro.build.date.utc",
            "ro.product.cpu.abi",
            "ro.baseband",
            "ro.boot.hardware",
        ]

        for prop in properties:
            success, output = self.execute_command(f"shell getprop {prop}", device_id)
            if success:
                info[prop] = output

        return info

    def get_battery_info(self, device_id: str) -> Dict[str, str]:
        """
        Get battery information
        Args:
            device_id: Device ID
        Returns:
            Dictionary of battery properties
        """
        success, output = self.execute_command("shell dumpsys battery", device_id)
        if not success:
            return {}

        battery_info = {}
        for line in output.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                battery_info[key.strip()] = value.strip()

        return battery_info

    def get_root_status(self, device_id: str) -> Dict[str, bool]:
        """
        Check root status
        Args:
            device_id: Device ID
        Returns:
            Dictionary of root status checks
        """
        status = {
            "shell_su": False,
            "binary_magisk": False,
            "binary_su": False,
            "app_magisk": False,
            "app_supersu": False,
        }

        # Check for su binary
        success, _ = self.execute_command("shell which su", device_id)
        status["shell_su"] = success

        # Check for Magisk binary
        success, _ = self.execute_command("shell test -f /system/xbin/magisk", device_id)
        status["binary_magisk"] = success

        # Check for su binary at standard location
        success, _ = self.execute_command("shell test -f /system/xbin/su", device_id)
        status["binary_su"] = success

        return status

    def disable_updates(self, device_id: str) -> bool:
        """
        Disable automatic system updates
        Args:
            device_id: Device ID
        Returns:
            True if successful
        """
        commands = [
            "shell pm disable com.android.systemupdate",
            "shell pm disable com.android.providers.media",
        ]

        for cmd in commands:
            success, output = self.execute_command(cmd, device_id)
            if not success:
                logger.warning(f"Failed to execute: {cmd}")

        return True

    def factory_reset(self, device_id: str, confirm: bool = False) -> bool:
        """
        Perform factory reset
        Args:
            device_id: Device ID
            confirm: Confirmation flag
        Returns:
            True if successful
        """
        if not confirm:
            return False

        success, output = self.execute_command("shell recovery --wipe_data", device_id)
        return success

    def wipe_cache(self, device_id: str) -> bool:
        """
        Wipe device cache
        Args:
            device_id: Device ID
        Returns:
            True if successful
        """
        success, output = self.execute_command("shell rm -rf /cache/*", device_id)
        return success

    def enable_developer_mode(self, device_id: str) -> bool:
        """
        Enable developer mode
        Args:
            device_id: Device ID
        Returns:
            True if successful
        """
        commands = [
            "shell settings put global development_settings_enabled 1",
            "shell settings put secure adb_enabled 1",
        ]

        for cmd in commands:
            success, _ = self.execute_command(cmd, device_id)
            if not success:
                return False

        return True

    def pull_file(self, device_id: str, source: str, destination: str) -> bool:
        """
        Pull file from device
        Args:
            device_id: Device ID
            source: Source path on device
            destination: Destination path on PC
        Returns:
            True if successful
        """
        success, output = self.execute_command(f"pull {source} {destination}", device_id)
        return success

    def push_file(self, device_id: str, source: str, destination: str) -> bool:
        """
        Push file to device
        Args:
            device_id: Device ID
            source: Source path on PC
            destination: Destination path on device
        Returns:
            True if successful
        """
        success, output = self.execute_command(f"push {source} {destination}", device_id)
        return success

    def reboot_device(self, device_id: str, mode: str = "system") -> bool:
        """
        Reboot device
        Args:
            device_id: Device ID
            mode: 'system', 'recovery', or 'bootloader'
        Returns:
            True if successful
        """
        if mode == "recovery":
            cmd = "reboot recovery"
        elif mode == "bootloader":
            cmd = "reboot bootloader"
        else:
            cmd = "reboot"

        success, output = self.execute_command(cmd, device_id)
        return success
