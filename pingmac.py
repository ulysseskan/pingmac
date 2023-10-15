"""Pings an IP every hour, if it's not responsive, notify using macOS notification"""

import os
import time
import subprocess

def show_mac_notification(title, message):
    """Show a notification on macOS"""
    script = f'display notification "{message}" with title "{title}"'
    os.system(f'echo -e "\\a"; osascript -e \'{script}\'')

def is_host_responsive(ip_address):
    """Check if the given IP address is responsive."""
    try:
        # Run ping command and capture output
        output = subprocess.check_output(['ping', '-c', '4', ip_address], \
                                         stderr=subprocess.STDOUT, text=True)
        # Extract response time from the output
        response_time = output.splitlines()[-1].split()[-2][5:]
        return True, response_time
    except subprocess.CalledProcessError:
        return False, None

def main():
    """define IP and execute checks every hour"""
    ip_address = "192.168.7.152"

    while True:
        is_responsive, response_time = is_host_responsive(ip_address)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        if is_responsive:
            print(f'{current_time} - {ip_address} is responsive. Response Time: {response_time} ms')
        else:
            print(f'{current_time} - {ip_address} is not responsive. Sending notification...')
            show_mac_notification('Network Status', \
                            f'{ip_address} is not responsive. Response Time: {response_time} ms')
        time.sleep(3600)  # Check every hour (3600 seconds)

if __name__ == "__main__":
    main()
