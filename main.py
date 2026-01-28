import cv2
import numpy as np
import pyautogui
import websockets
import json
import asyncio
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global variable to store screenshot path
screenshot_path = "screenshots/sober_compressed.png"

def find_color_in_image(image_path, hex_color):
    """Find the location of the color in the image and return the coordinates."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Load image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a mask where the color is present
    lower_bound = np.array(rgb, dtype=np.uint8)
    upper_bound = np.array(rgb, dtype=np.uint8)

    mask = cv2.inRange(image_rgb, lower_bound, upper_bound)
    coords = np.column_stack(np.where(mask > 0))

    return coords

def simulate_click_on_button(coords):
    """Simulate a mouse click on the button at the given coordinates."""
    if len(coords) > 0:
        x, y = coords[0]
        pyautogui.click(x, y)

@app.route('/find_color_and_click', methods=['POST'])
def find_color_and_click():
    """Endpoint that receives HEX color and simulates a click."""
    data = request.json
    hex_color = data.get("hex_color")

    if not hex_color:
        return jsonify({"error": "No color provided"}), 400

    coords = find_color_in_image(screenshot_path, hex_color)

    if len(coords) == 0:
        return jsonify({"error": "Color not found in the screenshot"}), 404

    # Simulate click
    simulate_click_on_button(coords)

    return jsonify({"status": "Clicked on the color"}), 200

# WebSocket server to listen for color clicks
async def handle_websocket(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        hex_color = data.get("hex_color")
        coords = find_color_in_image(screenshot_path, hex_color)
        if len(coords) > 0:
            simulate_click_on_button(coords)
            await websocket.send("Click simulated successfully!")
        else:
            await websocket.send("Color not found!")

async def websocket_server():
    server = await websockets.serve(handle_websocket, "localhost", 5000)
    await server.wait_closed()

# Run Flask app and WebSocket server simultaneously
def run_servers():
    loop = asyncio.get_event_loop()

    # Start Flask server
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(debug=False, host='0.0.0.0', port=5000))
    flask_thread.start()

    # Start WebSocket server
    loop.run_until_complete(websocket_server())

if __name__ == '__main__':
    run_servers()
