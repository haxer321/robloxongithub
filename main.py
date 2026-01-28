import subprocess
import requests
import time

# URL of the Replit backend where the image will be sent
REPLIT_URL = "https://49be1d29-103d-4e55-862a-72c64cec93d2-00-6hgk7i2x77bs.worf.replit.dev/upload"

def capture_and_send():
    while True:
        # Capture screenshot using ImageMagick (import command) on virtual display
        subprocess.run(["import", "-window", "root", "screenshot.png"], check=True)

        # Open the screenshot and send it to Replit backend
        with open("screenshot.png", "rb") as img_file:
            img_data = img_file.read()
            # Send the screenshot as a POST request
            response = requests.post(REPLIT_URL, files={"file": img_data})
            print(f"Sent screenshot: {response.status_code}")
        
        # Wait before capturing the next screenshot
        time.sleep(5)

if __name__ == "__main__":
    capture_and_send()
