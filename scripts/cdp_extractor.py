import paramiko
import openpyxl
import re

# Prompt for username, password, and devices.txt file path
username = input("Enter your SSH username: ")
password = input("Enter your SSH password: ")
device_file = input("Enter the path to your devices.txt file: ")

# List of device credentials (from the provided file)
device_list = []

# Read device IPs from the specified txt file
try:
    with open(device_file, 'r') as file:
        for line in file.readlines():
            device_list.append(line.strip())
except FileNotFoundError:
    print(f"Error: The file '{device_file}' was not found.")
    exit()

# Initialize workbook and worksheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = 'Cisco Devices'

# Set headers for the Excel sheet
sheet['A1'] = 'Device ID'
sheet['B1'] = 'IP Address'
sheet['C1'] = 'Platform'
sheet['D1'] = 'Neighbor Device ID'
sheet['E1'] = 'Neighbor IP Address'
sheet['F1'] = 'Neighbor Platform'
sheet['G1'] = 'Outgoing Interface'
sheet['H1'] = 'Outgoing Port'

# Function to login to Cisco device and fetch data using Paramiko
def get_device_info(ip_address):
    try:
        # Create SSH client instance
        ssh_client = paramiko.SSHClient()

        # Automatically add the server's SSH key (to avoid prompts for unknown host)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the device
        ssh_client.connect(ip_address, username=username, password=password, timeout=30)

        # Fetch the device platform using "show version"
        stdin, stdout, stderr = ssh_client.exec_command('show version')
        version_output = stdout.read().decode('utf-8')

        # Regex pattern to extract platform info (model or platform)
        platform_match = re.search(r"Model number\s+:\s+(\S+)", version_output)
        platform = platform_match.group(1) if platform_match else "Unknown"

        # Run the 'show cdp neighbor detail' command
        stdin, stdout, stderr = ssh_client.exec_command('show cdp neighbor detail')
        output = stdout.read().decode('utf-8')

        # Extract relevant neighbor information using regex
        neighbors = []
        neighbor_matches = re.findall(
            r'Device ID: (\S+).*?IP address: (\S+).*?Platform: (\S+).*?Interface: (\S+)', output, re.DOTALL)

        # Store the neighbor details
        for match in neighbor_matches:
            neighbors.append(match)

        ssh_client.close()

        return platform, neighbors

    except Exception as e:
        print(f"Failed to connect to {ip_address}: {e}")
        return None, None

# Loop through devices and fetch information
row = 2  # Starting row in the Excel sheet
for ip in device_list:
    platform, neighbors = get_device_info(ip)
    
    if neighbors:
        for neighbor in neighbors:
            # Write the information for each neighbor to the Excel sheet
            sheet[f'A{row}'] = ip  # Device ID (IP of current device)
            sheet[f'B{row}'] = ip  # IP Address (of current device)
            sheet[f'C{row}'] = platform  # Platform (current device platform)
            sheet[f'D{row}'] = neighbor[0]  # Neighbor Device ID
            sheet[f'E{row}'] = neighbor[1]  # Neighbor IP Address
            sheet[f'F{row}'] = neighbor[2]  # Neighbor Platform
            sheet[f'G{row}'] = neighbor[3]  # Outgoing Interface
            sheet[f'H{row}'] = neighbor[3]  # Outgoing Port (same as Interface for now)
            row += 1

# Adjust column widths and wrap text for better readability
for col in range(1, 9):  # Adjust columns A to H
    max_length = 0
    column = openpyxl.utils.get_column_letter(col)
    for row in sheet.iter_rows():
        try:
            cell_value = str(row[col-1].value)
            max_length = max(max_length, len(cell_value))
        except:
            pass
    adjusted_width = (max_length + 2)
    sheet.column_dimensions[column].width = adjusted_width

# Save the workbook to a file
workbook.save('device_info.xlsx')
print("Data extraction complete. Saved to 'device_info.xlsx'.")
