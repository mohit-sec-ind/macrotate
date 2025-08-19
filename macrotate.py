#!/usr/bin/env python3
import os
import time
import subprocess
import signal
import sys

# Set your network interface here
INTERFACE = "wlan0"   # change to eth0 if using Ethernet

def restore_mac():
    """Restore the permanent/original MAC address."""
    try:
        subprocess.run(["ifconfig", INTERFACE, "down"], check=True)
        subprocess.run(["macchanger", "-p", INTERFACE], check=True)  # restore original MAC
        subprocess.run(["ifconfig", INTERFACE, "up"], check=True)
        print(f"[+] Restored original MAC address on {INTERFACE}")
    except Exception as e:
        print(f"[-] Failed to restore MAC: {e}")

def change_mac():
    """Assign a random MAC address."""
    try:
        subprocess.run(["ifconfig", INTERFACE, "down"], check=True)
        subprocess.run(["macchanger", "-r", INTERFACE], check=True)
        subprocess.run(["ifconfig", INTERFACE, "up"], check=True)
        print(f"[+] MAC address changed for {INTERFACE}")
    except Exception as e:
        print(f"[-] Error: {e}")

def signal_handler(sig, frame):
    """Handle Ctrl+C and restore MAC."""
    print("\n[!] Caught Ctrl+C, restoring original MAC...")
    restore_mac()
    sys.exit(0)

def main():
    # Attach the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"[+] Starting MAC rotation every 180s on {INTERFACE}")
    while True:
        change_mac()
        time.sleep(180)  # wait 3 minutes

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[-] Run this script as root!")
        exit(1)
    main()
