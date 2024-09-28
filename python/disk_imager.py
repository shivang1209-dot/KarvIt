import subprocess
import urllib.request
import os
import psutil
import argparse

win32diskimager_path = "Win32DiskImager-Installer.exe"

def is_usb_connected():
    partitions = psutil.disk_partitions(all=True)
    external_drives = [partition.device for partition in partitions if 'removable' in partition.opts.lower()]
    if external_drives:
        print("External flash drives connected: ")
        for drive in external_drives:
            print(f"{drive}")
        return external_drives
    else:
        print("No external flash drives found.")
        return []

def is_win32diskimager_installed():
    global win32diskimager_path
    try:
        expected_size = 12567188
        actual_size = os.path.getsize(win32diskimager_path)
        if os.path.isfile(win32diskimager_path) and expected_size == actual_size:
            return True
        else:
            return False
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

def download_installer(url, path):
    try:
        print("Installing Win32DiskImager...")
        urllib.request.urlretrieve(url, path)
        print("Win32DiskImager successfully installed.")
    except Exception as e:
        print(f"Installation failed: {e}")

def download_and_install_win32diskimager():
    # Specify the URL of the Win32DiskImager installer
    win32diskimager_url = "https://win32diskimager.b-cdn.net/win32diskimager-1.0.0-install.exe"
    win32diskimager_path = "Win32DiskImager-Installer.exe"
    
    # Download the installer
    download_installer(win32diskimager_url, win32diskimager_path)

def create_disk_image(source_usb_drive, destination_image):
    try:
        subprocess.run([win32diskimager_path, 'drive_image.dd', source_usb_drive, '--output', destination_image], shell=True, check=True)
        print("Disk image created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating disk image: {e}")

def main():
    parser = argparse.ArgumentParser(description="CLI for creating a disk image using Win32DiskImager.")
    
    parser.add_argument(
        "--install", 
        action="store_true", 
        help="Download and install Win32DiskImager"
    )
    
    parser.add_argument(
        "--verify", 
        action="store_true", 
        help="Verify if Win32DiskImager is installed"
    )
    
    parser.add_argument(
        "--create-image", 
        type=str, 
        metavar="DRIVE", 
        help="Create a disk image from the specified USB drive (e.g., E:)"
    )
    
    args = parser.parse_args()

    if args.install:
        download_and_install_win32diskimager()

    if args.verify:
        if is_win32diskimager_installed():
            print("Win32DiskImager is installed.")
        else:
            print("Win32DiskImager is not installed. Use --install to download it.")

    if args.create_image:
        drive = args.create_image
        destination_image = 'usb_drive_image.img'
        create_disk_image(drive, destination_image)

if __name__ == "__main__":
    main()
