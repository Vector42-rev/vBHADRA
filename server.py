from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
from ultralytics import YOLO

app = Flask(__name__)
#model = YOLO(r"D:\dlcv\rtdet_l\kaggle\working\rtdetr_train\experiment1\weights\best.pt")
#model = YOLO(r"D:\dlcv\assignment\L7\yolo_8x_penis\kaggle\working\runs\detect\train\weights\best.pt")
model= YOLO(r"D:\dlcv\assignment\L5\yolo_8x_new\kaggle\working\runs\detect\train\weights\best.pt")

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    img = Image.open(io.BytesIO(file.read())).convert("RGB")
    results = model(img)

    top_boxes = []
    if results and results[0].boxes is not None:
        boxes = results[0].boxes
        scores = boxes.conf.cpu().numpy()
        sorted_indices = scores.argsort()[::-1][:3]  # top 10 or fewer
        for i in sorted_indices:
            box = boxes.xyxy[i].cpu().numpy().tolist()
            conf = float(scores[i])
            cls_id = int(boxes.cls[i])
            top_boxes.append({
                'class_id': cls_id,
                'confidence': conf,
                'bbox': box  # [x1, y1, x2, y2]
            })

    # Encode annotated image
    annotated_frame = results[0].plot()
    annotated_img = Image.fromarray(annotated_frame)
    img_io = io.BytesIO()
    annotated_img.save(img_io, 'JPEG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode('utf-8')

    return jsonify({
        'boxes': top_boxes,
        'image_base64': img_base64
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
