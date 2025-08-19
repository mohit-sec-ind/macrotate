#!/usr/bin/env python3
import os
import time
import subprocess

# Set your network interface here (check with: ip link show)
INTERFACE = "wlan0"   # change to eth0 if using Ethernet

def change_mac():
    try:
        # Bring interface down
        subprocess.run(["ifconfig", INTERFACE, "down"], check=True)
        
        # Randomize MAC using macchanger
        subprocess.run(["macchanger", "-r", INTERFACE], check=True)
        
        # Bring interface back up
        subprocess.run(["ifconfig", INTERFACE, "up"], check=True)
        
        print(f"[+] MAC address changed for {INTERFACE}")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    print(f"[+] Starting MAC rotation every 60s on {INTERFACE}")
    while True:
        change_mac()
        time.sleep(60)  # wait 1 minute

if __name__ == "__main__":
    # Ensure root privileges
    if os.geteuid() != 0:
        print("[-] Run this script as root!")
        exit(1)
    main()
