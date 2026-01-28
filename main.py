import time
import requests
import subprocess

def capture_and_send():
    while True:
        # Capture screenshot using ImageMagick and store it as screenshot.png
        subprocess.run(["import", "-window", "root", "screenshot.png"], check=True)

        # Send the screenshot to the Replit backend
        with open("screenshot.png", "rb") as img_file:
            files = {"image": img_file}
            response = requests.post("https://49be1d29-103d-4e55-862a-72c64cec93d2-00-6hgk7i2x77bs.worf.replit.dev/upload", files=files)
            if response.status_code == 200:
                print("Screenshot sent successfully")
            else:
                print("Failed to send screenshot")

        # Wait for 1 second before taking the next screenshot
        time.sleep(1)

capture_and_send()
