from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
from io import BytesIO
import base64
from gtts import gTTS
import os
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer

app = Flask(__name__)

# Define directories for saving images and audio
UPLOAD_FOLDER = 'static/uploads'
AUDIO_FOLDER = 'static/audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Load the pre-downloaded model
local_model_dir = "./pretrained_model"
model = VisionEncoderDecoderModel.from_pretrained(local_model_dir)
feature_extractor = ViTFeatureExtractor.from_pretrained(local_model_dir)
tokenizer = AutoTokenizer.from_pretrained(local_model_dir)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate-caption", methods=["POST"])
def generate_caption():
    try:
        # Extract image data from request
        data = request.json
        image_data = data.get("image_data")
        if not image_data:
            return jsonify({"error": "No image data received"}), 400

        # Decode and save the image
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        image_path = os.path.join(UPLOAD_FOLDER, "captured_image.png")
        image.save(image_path)

        # Generate caption
        image = image.convert("RGB")  # Ensure RGB mode
        inputs = feature_extractor(images=image, return_tensors="pt")
        outputs = model.generate(inputs.pixel_values)
        caption = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Convert caption to audio
        tts = gTTS(caption)
        audio_path = os.path.join(AUDIO_FOLDER, "caption_audio.mp3")
        tts.save(audio_path)

        # Return caption and audio path
        return jsonify({"caption": caption, "audio_path": f"/static/audio/caption_audio.mp3"})
    except Exception as e:
        print(f"Error generating caption: {e}")
        return jsonify({"error": "An error occurred while processing the image."}), 500

# Serve static files for images and audio
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
