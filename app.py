from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
from io import BytesIO
import base64
import os
from gtts import gTTS
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
from ultralytics import YOLO  # Fast YOLOv8 model
from pyngrok import ngrok

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
AUDIO_FOLDER = 'static/audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Load Models
caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

yolo_model = YOLO("yolov8n.pt")  # Use YOLOv8 nano model (fastest)

@app.after_request
def add_ngrok_header(response):
    # Add the custom header to skip ngrok's browser warning
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response


@app.route("/")
def home():
    return render_template("index1.html")



@app.route("/generate-caption", methods=["POST"])
def generate_caption():
    try:
        data = request.json
        image_data = data.get("image_data")
        if not image_data:
            return jsonify({"error": "No image data received"}), 400

        # Decode and save the image
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image_path = os.path.join(UPLOAD_FOLDER, "captured_image.png")
        image.save(image_path)

        # Generate Image Caption (Fast)
        inputs = feature_extractor(images=image, return_tensors="pt")
        outputs = caption_model.generate(inputs.pixel_values)
        caption = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Object Detection (Fast with YOLOv8)
        results = yolo_model(image_path)  # Run YOLO detection
        detected_objects = list(set([yolo_model.names[int(obj[5])] for obj in results[0].boxes.data]))  # Unique object names

        detected_text = ", ".join(detected_objects) if detected_objects else "No objects detected"

        # Convert Caption & Objects to Speech
        final_text = f"Caption: {caption}. Detected objects: {detected_text}"
        tts = gTTS(final_text)
        audio_path = os.path.join(AUDIO_FOLDER, "caption_audio.mp3")
        tts.save(audio_path)

        return jsonify({
            "caption": caption,
            "detected_objects": detected_text,
            "audio_path": f"/static/audio/caption_audio.mp3"
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing the image."}), 500

if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    print(f"ngrok tunnel available at: {public_url}")

    # Run Flask app
    app.run(port=5000)
