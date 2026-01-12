import requests
import base64
from PIL import Image
import io
import pyautogui
import subprocess
from datetime import datetime

YOLO_INPUT_SIZE = 640  # set to your model’s input dimension


def take_screenshot():
    """Capture the full screen."""
    return pyautogui.screenshot()


def correct_for_letterbox(x1, y1, x2, y2, orig_w, orig_h, model_w, model_h):
    """
    Correct YOLO coordinates for letterboxing (black padding added to maintain aspect ratio).
    """
    r = min(model_w / orig_w, model_h / orig_h)
    new_w, new_h = orig_w * r, orig_h * r
    pad_x = (model_w - new_w) / 2
    pad_y = (model_h - new_h) / 2

    # remove padding, scale back to original image size
    x1 = (x1 - pad_x) / r
    y1 = (y1 - pad_y) / r
    x2 = (x2 - pad_x) / r
    y2 = (y2 - pad_y) / r

    return [x1, y1, x2, y2]


def map_to_screen(x1, y1, x2, y2, img_w, img_h, screen_w, screen_h):
    """Map corrected YOLO coordinates to actual screen coordinates."""
    scale_x = screen_w / img_w
    scale_y = screen_h / img_h
    return [
        int(x1 * scale_x),
        int(y1 * scale_y),
        int(x2 * scale_x),
        int(y2 * scale_y)
    ]


def send_screenshot_to_server(screenshot, server_url='http://localhost:5000/detect'):
    """Send screenshot to YOLO detection server and blackout detected regions."""
    img_io = io.BytesIO()
    screenshot.save(img_io, format='JPEG')
    img_io.seek(0)
    files = {'image': ('screenshot.jpg', img_io, 'image/jpeg')}
    response = requests.post(server_url, files=files)

    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text}")
        return

    data = response.json()
    boxes = data.get('boxes', [])
    print(f"\n✅ Detected {len(boxes)} objects")

    # Save annotated image (for debugging)
    if 'image_base64' in data:
        annotated_data = base64.b64decode(data['image_base64'])
        annotated_img = Image.open(io.BytesIO(annotated_data))
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        annotated_img.save(f"annotated_{ts}.jpg")

    if not boxes:
        print("No detections, skipping blackout.")
        return

    img_w, img_h = screenshot.size
    screen_w, screen_h = pyautogui.size()

    for box in boxes:
        x1, y1, x2, y2 = box['bbox']
        x1, y1, x2, y2 = correct_for_letterbox(x1, y1, x2, y2, img_w, img_h, YOLO_INPUT_SIZE, YOLO_INPUT_SIZE)
        sx1, sy1, sx2, sy2 = map_to_screen(x1, y1, x2, y2, img_w, img_h, screen_w, screen_h)

        print(f"Launching blackout.exe {sx1} {sy1} {sx2} {sy2}")
        subprocess.Popen(
            ['blackout.exe', str(sx1), str(sy1), str(sx2), str(sy2)],
            shell=True
        )


if __name__ == "__main__":
    print("🟢 Automatic screenshot mode. Press Ctrl+C to stop.")
    try:
        while True:
            screenshot = take_screenshot()
            send_screenshot_to_server(screenshot)
    except KeyboardInterrupt:
        print("\n🟥 Stopped by user.")
