Cisco CDP Topology Extractor

A Python-based automation tool that connects to Cisco network devices via SSH, collects CDP neighbor topology, and exports all discovered data into a structured Excel file. This tool is ideal for network engineers, NOC teams, and automation specialists who want to automate network discovery and documentation.

🚀 Features

Connects to multiple Cisco devices via SSH

Extracts CDP neighbor details from each device

Captures platform, neighbor IDs, neighbor IPs, and outgoing interfaces

Creates a structured Excel report (device_info.xlsx)

Handles connectivity failures gracefully

Includes sample device list

Professional error handling and logging output

Compatible with Windows, Linux, and macOS

📦 Project Structure

cisco-cdp-topology-extractor/ │ ├── scripts/ │ └── cdp_extractor.py # Main Python script │ ├── samples/ │ └── devices.txt # Example list of device IPs │ ├── output/ │ └── device_info.xlsx # Excel output (generated after run) │ ├── requirements.txt # Required Python packages │ └── README.md # Documentation 

🛠 Requirements

Python 3.8+

Cisco devices with CDP enabled

SSH accessibility

Python modules:

paramiko

openpyxl

Install dependencies:

pip install -r requirements.txt 

⚙️ Usage

1. Prepare device list

Edit the file:

samples/devices.txt 

Insert device IP addresses:

10.10.10.1 10.10.10.2 10.10.10.3 

2. Run the extractor

python3 scripts/cdp_extractor.py 

3. Provide credentials when prompted:

Enter your SSH username: admin Enter your SSH password: ******** Enter the path to your devices.txt file: samples/devices.txt 

4. Output

A complete Excel file is generated at:

output/device_info.xlsx 

🧪 Example Output (Excel Columns)

Device IPPlatformNeighbor Device IDNeighbor IPNeighbor PlatformOutgoing InterfaceOutgoing Port 

🧰 How It Works

The script reads the list of IPs.

It SSHs into each Cisco device using Paramiko.

Runs:

show version

show cdp neighbor detail

Parses platform details using regex.

Extracts CDP neighbor information.

Stores all results in Excel.

Automatically adjusts column widths.

🔐 Security Notes

Avoid using plain-text credentials in production.

Restrict SSH access using ACLs or firewalls.

Consider enabling SSH key authentication.

CDP exposes neighbor information — use securely.

🐛 Troubleshooting

❌ Cannot connect to device

Verify SSH is enabled: show run | i ssh

Ensure IP is reachable

Check credentials

❌ No CDP neighbors found

Ensure CDP is enabled:

show cdp neighbors 

Or enable globally:

cdp run 

🚧 Future Enhancements

Add LLDP support

Visualize topology using Graphviz

Export JSON and CSV formats

Generate a network map PNG

Multi-threading for faster execution

📜 License

MIT License

🤝 Contributions

Pull requests are welcome!

⭐ If you find this project useful

Please consider starring the repository to support development!
