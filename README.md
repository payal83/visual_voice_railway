---

# **Flask App: Image Captioning with Audio Generation**

This project is a Flask-based web application that performs image captioning using a pre-trained vision-language model (`ViT-GPT2`) and generates audio output for the captions using Google Text-to-Speech (`gTTS`). Users can upload an image, receive a text-based caption, and download an audio file of the caption.

---

## **Features**
- Upload an image to generate a descriptive caption.
- Generate an audio version of the caption.
- View and download the caption audio from the browser.

---

## **Tech Stack**
- **Backend**: Flask
- **Machine Learning**: 
  - `VisionEncoderDecoderModel` from Hugging Face Transformers
  - `ViTFeatureExtractor` for image processing
  - `AutoTokenizer` for text generation
- **Text-to-Speech**: Google Text-to-Speech (`gTTS`)
- **Image Processing**: Pillow (`PIL`)

---

## **Project Structure**
```
my-flask-app/
│
├── app.py               # Main Flask application
├── requirements.txt     # Dependencies for the project
├── static/              # Folder for static files
│   ├── uploads/         # Directory for uploaded images
│   └── audio/           # Directory for generated audio files
├── templates/
│   └── index.html       # HTML file for the homepage
└── README.md            # Project documentation (this file)
```

---

## **Setup and Installation**

### 1. **Clone the Repository**
```bash
git clone <repository_url>
cd my-flask-app
```

### 2. **Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate    # On Windows, use `venv\Scripts\activate`
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Run the App**
```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000`.

---

## **Endpoints**

### 1. **Homepage**
- **URL**: `/`
- **Method**: `GET`
- **Description**: Displays the homepage with an upload form.

### 2. **Generate Caption**
- **URL**: `/generate-caption`
- **Method**: `POST`
- **Description**: Accepts a base64-encoded image and returns:
  - A generated caption.
  - A link to the audio file of the caption.
- **Request Body** (JSON):
  ```json
  {
    "image_data": "data:image/png;base64,...."
  }
  ```
- **Response** (JSON):
  ```json
  {
    "caption": "A descriptive caption of the image.",
    "audio_path": "/static/audio/caption_audio.mp3"
  }
  ```

---

## **Static File Serving**
- Uploaded images are saved in the `static/uploads` folder.
- Generated audio files are saved in the `static/audio` folder.

---

## **Customization**

### Change Directories
- Update the directories for image and audio storage by modifying the `UPLOAD_FOLDER` and `AUDIO_FOLDER` variables in `app.py`.

### Modify the Model
- Replace the pre-trained model (`nlpconnect/vit-gpt2-image-captioning`) with any compatible Hugging Face model:
  ```python
  model = VisionEncoderDecoderModel.from_pretrained("your-model-name")
  ```

---

## **Example Workflow**
1. Access the app at `http://127.0.0.1:5000`.
2. Upload an image through the form.
3. Receive a caption and an audio file.

---

## **Deployment**
For deployment on platforms like Railway, ensure:
1. All files are included in the repository.
2. Update `requirements.txt` and `runtime.txt` (if applicable).
3. Configure the start command:
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```

---

## **Dependencies**
Listed in `requirements.txt`:
```
Flask==2.3.2
Pillow==9.5.0
transformers==4.30.2
torch==2.0.1
gtts==2.3.2
```

---

## **Acknowledgements**
- Hugging Face for the pre-trained models.
- Google Text-to-Speech for audio generation.

---

Feel free to customize this file as per your needs! Let me know if you need further clarification or help with deployment.
