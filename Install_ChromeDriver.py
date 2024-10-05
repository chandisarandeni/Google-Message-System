import os
import platform
import requests
import zipfile
import subprocess
from pathlib import Path

def get_chrome_version():
    """Get the installed version of Chrome."""
    if platform.system() == "Windows":
        version = subprocess.check_output(
            r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get version /value', shell=True
        ).decode().strip().split('=')[1]
    elif platform.system() == "Darwin":  # macOS
        version = subprocess.check_output(
            ['/Applications/Google Chrome.app/Contents/Info.plist', '-r', 'CFBundleShortVersionString'], shell=True
        ).decode().strip()
    elif platform.system() == "Linux":
        version = subprocess.check_output(
            "google-chrome --version", shell=True
        ).decode().strip().split()[-1]
    else:
        raise Exception("Unsupported OS")
    
    return version

def get_chromedriver_version():
    """Get the installed version of ChromeDriver."""
    chromedriver_path = Path("chromedriver.exe" if platform.system() == "Windows" else "chromedriver")
    if chromedriver_path.exists():
        version = subprocess.check_output(
            [str(chromedriver_path), "--version"]
        ).decode().strip().split()[1]
        return version
    return None

def download_chromedriver(version):
    """Download ChromeDriver for the specified version."""
    system_platform = platform.system()
    if system_platform == "Windows":
        download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
    elif system_platform == "Darwin":  # macOS
        download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_mac64.zip"
    elif system_platform == "Linux":
        download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip"
    else:
        raise Exception("Unsupported OS")

    print(f"Downloading ChromeDriver from: {download_url}")
    
    response = requests.get(download_url)
    
    if response.status_code != 200:
        print(f"Failed to download ChromeDriver version {version}. Trying to find the latest available version.")
        latest_version = fetch_latest_chromedriver()
        print(f"Falling back to latest available ChromeDriver version: {latest_version}")
        download_chromedriver(latest_version)
        return

    with open("chromedriver.zip", "wb") as file:
        file.write(response.content)

    if not zipfile.is_zipfile("chromedriver.zip"):
        raise Exception("Downloaded file is not a valid zip file.")

def fetch_latest_chromedriver():
    """Fetch the latest available ChromeDriver version."""
    try:
        url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            raise Exception("Could not fetch the latest ChromeDriver version.")
    except Exception as e:
        raise Exception(f"Error fetching latest ChromeDriver version: {e}")

def extract_chromedriver():
    """Extract the downloaded ChromeDriver ZIP file."""
    with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
        zip_ref.extractall(".")

    chromedriver_path = Path("chromedriver.exe" if platform.system() == "Windows" else "chromedriver")

    if not chromedriver_path.exists():
        raise Exception("ChromeDriver not found after extraction. Check the ZIP file contents.")

def move_chromedriver():
    """Move ChromeDriver to a specific directory and set permissions."""
    if platform.system() == "Windows":
        target_path = Path(os.path.expanduser("~/chromedriver/chromedriver.exe"))
    else:
        target_path = Path("/usr/local/bin/chromedriver")

    current_path = Path("chromedriver.exe" if platform.system() == "Windows" else "chromedriver")

    if not current_path.exists():
        raise Exception("ChromeDriver not found after extraction.")

    os.makedirs(target_path.parent, exist_ok=True)
    os.rename(current_path, target_path)

    print(f"ChromeDriver installed at: {target_path}")

def main():
    try:
        print("Checking installed Chrome version...")
        chrome_version = get_chrome_version()
        print(f"Using Chrome version: {chrome_version}")

        print("Checking installed ChromeDriver version...")
        installed_chromedriver_version = get_chromedriver_version()

        if installed_chromedriver_version is None:
            print("ChromeDriver not found. Downloading...")
            download_chromedriver(chrome_version)
            extract_chromedriver()
            move_chromedriver()
            print("ChromeDriver installation completed successfully.")
        else:
            print(f"Installed ChromeDriver version: {installed_chromedriver_version}")

            latest_chromedriver_version = fetch_latest_chromedriver()
            print(f"Latest available ChromeDriver version: {latest_chromedriver_version}")

            if installed_chromedriver_version < latest_chromedriver_version:
                print("Updating ChromeDriver to the latest version...")
                download_chromedriver(latest_chromedriver_version)
                extract_chromedriver()
                move_chromedriver()
                print("ChromeDriver update completed successfully.")
            else:
                print("ChromeDriver is up to date.")

        # Clean up the downloaded ZIP file
        os.remove("chromedriver.zip")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
