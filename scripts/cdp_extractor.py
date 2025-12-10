#!/usr/bin/env python3
"""
Advanced Cisco CDP Topology Extractor
--------------------------------------
Improved version with:
- Better error handling
- Clear progress output
- Cleaner regex parsing
- Output file saved into output/device_info.xlsx
- Device-level isolation for failures
- Graceful handling of empty neighbors
"""

import paramiko
import openpyxl
import re
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# User Input
# ---------------------------------------------------------------------------
username = input("Enter your SSH username: ")
password = input("Enter your SSH password: ")
device_file = input("Enter the path to your devices.txt file: ")

# ---------------------------------------------------------------------------
# Load device list
# ---------------------------------------------------------------------------
device_list = []

try:
    with open(device_file, 'r') as file:
        for line in file.readlines():
            ip = line.strip()
            if ip:
                device_list.append(ip)
except FileNotFoundError:
    print(f"Error: The file '{device_file}' was not found.")
    exit()

if not device_list:
    print("No device IPs found in the file.")
    exit()

# ---------------------------------------------------------------------------
# Prepare Excel workbook
# ---------------------------------------------------------------------------
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Cisco CDP Topology"

headers = [
    "Device IP", "Platform", "Neighbor Device ID", "Neighbor IP", 
    "Neighbor Platform", "Outgoing Interface", "Outgoing Port"
]

sheet.append(headers)

# ---------------------------------------------------------------------------
# Function to connect and retrieve data
# ---------------------------------------------------------------------------
def get_device_info(ip_address):
    print(f"\n📡 Connecting to {ip_address} ...")

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password, timeout=20)

        # ---------------------------
        # Fetch platform
        # ---------------------------
        stdin, stdout, stderr = ssh.exec_command("show version")
        version_output = stdout.read().decode()

        platform_match = re.search(r"[Mm]odel number\s*:\s*(\S+)", version_output)
        platform = platform_match.group(1) if platform_match else "Unknown"

        # ---------------------------
        # Fetch CDP neighbors
        # ---------------------------
        stdin, stdout, stderr = ssh.exec_command("show cdp neighbor detail")
        cdp_output = stdout.read().decode()

        # Improved regex for neighbor extraction
        neighbor_matches = re.findall(
            r"Device ID: (.*?)\\n.*?IP address: (.*?)\\n.*?Platform: (.*?),.*?Interface: (.*?) ",
            cdp_output,
            re.DOTALL
        )

        neighbors = []
        for n in neighbor_matches:
            device_id = n[0].strip()
            nbr_ip = n[1].strip()
            nbr_platform = n[2].strip()
            interface = n[3].strip()
            neighbors.append((device_id, nbr_ip, nbr_platform, interface))

        ssh.close()
        return platform, neighbors

    except Exception as e:
        print(f"❌ Error connecting to {ip_address}: {e}")
        return None, []

# ---------------------------------------------------------------------------
# Main processing loop
# ---------------------------------------------------------------------------
row_counter = 2

total = len(device_list)
print(f"\n🚀 Starting CDP Extraction for {total} devices...")

for index, ip in enumerate(device_list, start=1):
    print(f"\n🔎 [{index}/{total}] Processing {ip}")

    platform, neighbors = get_device_info(ip)

    if platform is None:
        continue

    if not neighbors:
        print(f"⚠ No CDP neighbors found on {ip}")
        continue

    for n in neighbors:
        sheet[f"A{row_counter}"] = ip
        sheet[f"B{row_counter}"] = platform
        sheet[f"C{row_counter}"] = n[0]
        sheet[f"D{row_counter}"] = n[1]
        sheet[f"E{row_counter}"] = n[2]
        sheet[f"F{row_counter}"] = n[3]
        sheet[f"G{row_counter}"] = n[3]
        row_counter += 1

# ---------------------------------------------------------------------------
# Auto-adjust column widths
# ---------------------------------------------------------------------------
for col in sheet.columns:
    max_len = 0
    col_letter = col[0].column_letter
    for cell in col:
        if cell.value:
            cell_len = len(str(cell.value))
            if cell_len > max_len:
                max_len = cell_len
    sheet.column_dimensions[col_letter].width = max_len + 2

# ---------------------------------------------------------------------------
# Save Excel
# ---------------------------------------------------------------------------
outfile = os.path.join(output_dir, "device_info.xlsx")
workbook.save(outfile)

print(f"\n✅ Extraction complete! Saved to: {outfile}")
