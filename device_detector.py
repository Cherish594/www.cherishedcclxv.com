#!/usr/bin/env python3
"""
Device Detector Module - Identifies device type and specifications
"""

import logging
from typing import Dict, Optional
from colorama import Fore, Style, init

init(autoreset=True)

logger = logging.getLogger(__name__)


class DeviceDetector:
    """Detects and classifies Android devices"""

    # Device database
    DEVICE_DATABASE = {
        "tecno": {
            "KL4": {
                "name": "Tecno Spark Go",
                "recovery_keys": ["VOLUME_UP", "POWER"],
                "fastboot_keys": ["VOLUME_DOWN", "POWER"],
                "support_frp_fix": True,
                "requires_root": False,
            },
            "KD7": {
                "name": "Tecno Spark 10",
                "recovery_keys": ["VOLUME_UP", "POWER"],
                "fastboot_keys": ["VOLUME_DOWN", "POWER"],
                "support_frp_fix": True,
            },
        },
        "samsung": {
            "A": {
                "name": "Samsung Galaxy A Series",
                "recovery_keys": ["VOLUME_UP", "POWER"],
                "fastboot_keys": ["VOLUME_DOWN", "POWER"],
                "support_frp_fix": True,
            },
            "S": {
                "name": "Samsung Galaxy S Series",
                "recovery_keys": ["VOLUME_UP", "POWER"],
                "fastboot_keys": ["VOLUME_DOWN", "POWER"],
                "support_frp_fix": True,
            },
        },
        "xiaomi": {
            "redmi": {
                "name": "Xiaomi Redmi Series",
                "recovery_keys": ["VOLUME_UP", "POWER"],
                "fastboot_keys": ["VOLUME_DOWN", "POWER"],
                "support_frp_fix": True,
            },
        },
    }

    def __init__(self):
        self.detected_device = None

    def detect_from_properties(self, device_props: Dict[str, str]) -> Optional[Dict]:
        """
        Detect device from properties
        Args:
            device_props: Dictionary of device properties
        Returns:
            Dictionary with device info
        """
        brand = device_props.get("ro.product.brand", "").lower()
        model = device_props.get("ro.product.model", "").upper()
        device_name = device_props.get("ro.product.device", "").lower()
        android_version = device_props.get("ro.build.version.release", "")
        sdk = device_props.get("ro.build.version.sdk", "")
        cpu_abi = device_props.get("ro.product.cpu.abi", "")
        serial = device_props.get("ro.serialno", "")

        device_info = {
            "brand": brand,
            "model": model,
            "device_name": device_name,
            "android_version": android_version,
            "sdk": sdk,
            "cpu_abi": cpu_abi,
            "serial": serial,
            "support_frp_fix": False,
            "recovery_keys": ["VOLUME_UP", "POWER"],
            "fastboot_keys": ["VOLUME_DOWN", "POWER"],
        }

        # Try to match with database
        if brand in self.DEVICE_DATABASE:
            for model_key, model_info in self.DEVICE_DATABASE[brand].items():
                if model_key.lower() in model.lower() or model_key.lower() in device_name.lower():
                    device_info.update(model_info)
                    device_info["matched"] = True
                    self.detected_device = device_info
                    return device_info

        self.detected_device = device_info
        return device_info

    def get_device_name(self, device_props: Dict[str, str]) -> str:
        """
        Get friendly device name
        Args:
            device_props: Device properties
        Returns:
            Device name string
        """
        detected = self.detect_from_properties(device_props)
        if detected and "name" in detected:
            return detected["name"]

        brand = device_props.get("ro.product.brand", "Unknown")
        model = device_props.get("ro.product.model", "Unknown")
        return f"{brand} {model}"

    def supports_frp_fix(self, device_props: Dict[str, str]) -> bool:
        """
        Check if device supports FRP fix
        Args:
            device_props: Device properties
        Returns:
            True if device supports FRP fix
        """
        detected = self.detect_from_properties(device_props)
        return detected.get("support_frp_fix", False)

    def get_recovery_method(self, device_props: Dict[str, str]) -> str:
        """
        Get recommended recovery method
        Args:
            device_props: Device properties
        Returns:
            Recovery method string
        """
        android_version = int(device_props.get("ro.build.version.sdk", 0))

        if android_version >= 31:  # Android 12+
            return "fastbootd"
        elif android_version >= 29:  # Android 10+
            return "recovery_sideload"
        else:
            return "traditional_recovery"

    def format_device_info(self, device_props: Dict[str, str]) -> str:
        """
        Format device info for display
        Args:
            device_props: Device properties
        Returns:
            Formatted string
        """
        output = []
        output.append(f"{Fore.CYAN}═══════════════════════════════════════{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}Device Information{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}═══════════════════════════════════════{Style.RESET_ALL}")

        brand = device_props.get("ro.product.brand", "N/A")
        model = device_props.get("ro.product.model", "N/A")
        device = device_props.get("ro.product.device", "N/A")
        serial = device_props.get("ro.serialno", "N/A")

        output.append(f"{Fore.GREEN}Model{Style.RESET_ALL}: {model}")
        output.append(f"{Fore.GREEN}Brand{Style.RESET_ALL}: {brand}")
        output.append(f"{Fore.GREEN}Device{Style.RESET_ALL}: {device}")
        output.append(f"{Fore.GREEN}Serial{Style.RESET_ALL}: {serial}")

        android_version = device_props.get("ro.build.version.release", "N/A")
        sdk = device_props.get("ro.build.version.sdk", "N/A")
        output.append(f"{Fore.GREEN}Android Version{Style.RESET_ALL}: {android_version}")
        output.append(f"{Fore.GREEN}SDK Level{Style.RESET_ALL}: {sdk}")

        cpu_abi = device_props.get("ro.product.cpu.abi", "N/A")
        output.append(f"{Fore.GREEN}CPU ABI{Style.RESET_ALL}: {cpu_abi}")

        fingerprint = device_props.get("ro.build.fingerprint", "N/A")
        output.append(f"{Fore.GREEN}Fingerprint{Style.RESET_ALL}: {fingerprint}")

        return "\n".join(output)
