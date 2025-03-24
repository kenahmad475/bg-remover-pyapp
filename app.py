from flask import Flask, request, send_file, render_template
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

# Ensure the upload and output directories exist
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400

    file = request.files['image']
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    output_path = os.path.join(app.config["OUTPUT_FOLDER"], f"output_{file.filename}")

    # Save input file
    file.save(input_path)

    # Process image
    image = Image.open(input_path)
    output_image = remove(image)

    # Save output file
    output_image.save(output_path, 'PNG')

    return send_file(output_path, as_attachment=True, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

