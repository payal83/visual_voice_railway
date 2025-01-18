from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
from io import BytesIO
import base64
from gtts import gTTS
import os
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
# Directories for saving images and audio
UPLOAD_FOLDER = 'static/uploads'
AUDIO_FOLDER = 'static/audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

model, feature_extractor, tokenizer = None, None, None
def load_model_resources():
    global model, feature_extractor, tokenizer
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate-caption", methods=["POST"])
def generate_caption():
    try:
        # Step 1: Load resources lazily
        load_model_resources()
        global model, feature_extractor, tokenizer
        # Step 2: Extract and validate image data
        data = request.json
        if not data or "image_data" not in data:
            return jsonify({"error": "Invalid request: No image data provided"}), 400

        image_data = data["image_data"]
        if "," not in image_data:
            return jsonify({"error": "Invalid image format"}), 400

        # Step 3: Decode and save the image
        image_data = image_data.split(",")[1]  # Remove data URI prefix
        image_bytes = base64.b64decode(image_data)
        try:
            image = Image.open(BytesIO(image_bytes))
            image = image.convert("RGB")  # Ensure RGB mode
        except Exception as e:
            return jsonify({"error": f"Failed to process image: {str(e)}"}), 400

        image_path = os.path.join(UPLOAD_FOLDER, "captured_image.png")
        image.save(image_path)

        # Step 4: Generate caption
        try:
            inputs = feature_extractor(images=image, return_tensors="pt")
            pixel_values = inputs.pixel_values
            outputs = model.generate(pixel_values)
            caption = tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            return jsonify({"error": f"Failed to generate caption: {str(e)}"}), 500

        # Step 5: Convert caption to audio
        try:
            tts = gTTS(caption)
            audio_path = os.path.join(AUDIO_FOLDER, "caption_audio.mp3")
            tts.save(audio_path)
        except Exception as e:
            return jsonify({"error": f"Failed to generate audio: {str(e)}"}), 500

        # Step 6: Return response
        return jsonify({"caption": caption, "audio_path": f"/static/audio/caption_audio.mp3"})
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# Serve static files for images and audio
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not defined
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
