from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def init_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start Chrome maximized

    # Automatically install the correct version of ChromeDriver
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    return driver

def main():
    driver = None
    try:
        driver = init_webdriver()
        print("Loading Google Messages...")
        driver.get("https://messages.google.com/web/authentication")

        # Wait for a few seconds to ensure the page loads
        time.sleep(10)  # Adjust this time if necessary

        # Wait for the user to scan the QR code and log in
        input("Please scan the QR code and press Enter to continue...")
        
        print("You are now logged in to Google Messages.")
        print("Press Enter to close the browser...")
        input()  # Wait for user to press Enter
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver is not None:
            driver.quit()

if __name__ == "__main__":
    main()
