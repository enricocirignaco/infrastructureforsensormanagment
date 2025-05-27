import sys
import argparse
import os
import subprocess
import platform
sys.path.insert(0, './bundled_libs/pyserial.zip')
from serial.tools import list_ports

# Heltec firmware flasher script
parser = argparse.ArgumentParser(description="Heltec firmware flasher")
parser.add_argument("binary_dir", help="Path to the directory containing the ELF and HEX files")
args = parser.parse_args()
binary_dir = args.binary_dir

# Platform-dependent tool paths
system = platform.system()
base_path = './tools'
elf_tool_name = 'CubeCellelftool'
flash_tool_name = 'CubeCellflash'
objcopy_tool_name = 'objcopy'
if system == "Darwin":
    os_folder = 'macos'
elif system == "Linux":
    os_folder = 'linux'
elif system == "Windows":
    os_folder = 'windows'
else:
    print(f"Unsupported OS: {system}")
    sys.exit(1)
elf_tool_path = os.path.join(base_path, elf_tool_name, os_folder, elf_tool_name + ('.exe' if system == 'Windows' else ''))
flash_tool_path = os.path.join(base_path, flash_tool_name, os_folder, flash_tool_name + ('.exe' if system == 'Windows' else ''))
objcopy_tool_path = os.path.join(base_path, objcopy_tool_name, os_folder, objcopy_tool_name + ('.exe' if system == 'Windows' else ''))
os.chmod(elf_tool_path, 0o755)
os.chmod(flash_tool_path, 0o755)
os.chmod(objcopy_tool_path, 0o755)

print("Checking for required firmware files (.elf and .hex)...")
# check if a hex and elf files are present in the directory
hex_files = [f for f in os.listdir(binary_dir) if f.lower().endswith(".hex")]
elf_files = [f for f in os.listdir(binary_dir) if f.lower().endswith(".elf")]
if len(hex_files) != 1 or len(elf_files) != 1:
    print("Error: directory must contain exactly one .hex and one .elf file.")
    sys.exit(1)

# generate cyacd file with CubeCell utiliy
hex_path = os.path.join(binary_dir, hex_files[0])
elf_path = os.path.join(binary_dir, elf_files[0])
print(f"Found ELF: {elf_path}")
print(f"Found HEX: {hex_path}")
cyacd_path = os.path.join(binary_dir, "firmware.cyacd")

gcc_path = '/Users/macbook/Desktop/tools/gcc-arm-none-eabi/8-2019-q3/bin'
# run the tool to generate the cyacd file
try:
    print("Generating .cyacd firmware file...")
    subprocess.run([
        elf_tool_path,
        objcopy_tool_path,
        elf_path,
        hex_path,
        cyacd_path
    ], check=True)
except subprocess.CalledProcessError as e:
    print("Error while generating .cyacd file:", e)
    sys.exit(1)

##############################################################
print(f"{cyacd_path} Successfully generated.")
response = input("Do you want to flash the firmware now? [y/N]: ").strip().lower()
if response != 'y':
    print("Aborting flash. Exiting.")
    sys.exit(0)
# Detect available serial ports for flashing
print("Detecting available serial ports...")
ports = list_ports.comports()
if not ports:
    print("No serial ports found.")
    exit(1)

print("Available serial ports:")
for i, port in enumerate(ports):
    print(f"[{i}] {port.device} — {port.description}")

print("Waiting for user to select a serial port...")
choice = int(input("Select the port number: "))
if choice < 0 or choice >= len(ports):
    print("Invalid port selection.")
    sys.exit(1)
selected_port = ports[choice].device
print(f"Selected port: {selected_port}")

# Flash the firmware using CubeCell utility
print("Flashing firmware...")
try:
    subprocess.run([
        flash_tool_path,
        "-serial", selected_port,
        cyacd_path
    ], check=True)
    print("Firmware flashed successfully.")
except subprocess.CalledProcessError as e:
    print("Error during firmware flashing:", e)
    sys.exit(1)
