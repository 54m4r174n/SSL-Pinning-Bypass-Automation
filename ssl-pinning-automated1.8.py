import os
import subprocess
import xml.etree.ElementTree as ET
import shutil

print(f"")
print(f"This script is used to automate a complete process of SSL Pinning and Root Detection Bypass.")
print(f"The Pre requisites for this script are as follows:")
print(f"The universal_root_ssl_bypass.js should be in this folder")
print(f"Nox player should be turned on and root should be on")
print(f"")

# Function to get the package name of an APK file
def get_package_name(apk_path):
    package_name = subprocess.check_output(['aapt', 'dump', 'badging', apk_path]).decode('utf-8').split("package: name='")[1].split("'")[0]
    return package_name

while True:
    apk_path = input("Enter APK file path (or 'quit' to exit): ")
    if apk_path == "quit":
        break

    # Check if the APK file exists
    if not os.path.isfile(apk_path):
        print(f"File '{apk_path}' does not exist.")
        continue

    # Ask user to enter the path of the APK file
    #apk_path = input("Please enter the path of the APK file: ")
    
    # Get the package name of the APK file
    package_name = get_package_name(apk_path)
    
    # Print the package name
    print("Package name:", package_name)

    # Running Nox
    #print(f"Opening Nox Player hoping you have the nox.exe in the C:/Program Files (x86)/Nox/bin/Nox.exe Path if not keep it here or modify the script to give correct path")
    #subprocess.run([r"C:\\Program Files (x86)\\Nox\\bin\\Nox.exe"])


    # Run the adb shell command to connect to the device
    print("Connecting to device with adb shell...")
    adb_process = subprocess.Popen(["adb", "shell"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    # Once connected to the device, navigate to the /data/local/tmp directory
    print("Navigating to /data/local/tmp directory...")
    adb_process.stdin.write(b"cd /data/local/tmp\n")
    adb_process.stdin.flush()

    # Run the frida-server-andro command using the ./frida-server-andro syntax
    print("Starting frida server...")
    adb_process.stdin.write(b"./frida-server-andro\n")
    adb_process.stdin.flush()


    # Use frida to run the ssl-pinning script
    print(f"Running frida with {package_name} and ssl-pinning script...")
    frida_command = f"frida -U -f {package_name} -l universal_root_ssl_bypass.js"
    subprocess.run(frida_command, shell=True)

print("Exiting script.")
