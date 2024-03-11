from flask import Flask, render_template, request, jsonify
import os
import csv
import json
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

# # Adding path to config
app.config['INITIAL_FILE_UPLOAD'] = 'static/uploads'

# Function to extract text from an image using EdenAI

OCR_ENDPOINT = "https://api.edenai.run/v1/pretrained/vision/ocr"

# Eden AI API key
API_KEY = "YOUR_EDEN_AI_API_KEY"

# Function to extract text from an image using Eden AI OCR API


def extract_text_from_image(image_file):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    files = {
        "files": image_file,
        "providers": ["microsoft", "aws", "google", "ibm"],
        "language": "en"
    }
    response = requests.post(OCR_ENDPOINT, files=files, headers=headers)
    if response.status_code == 200:
        return response.json().get("predictions")[0].get("ocr")
    else:
        return None

# Function to save extracted text to a CSV file


def save_to_csv(data, filename='output.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Text'])
        csv_writer.writerows([[text] for text in data])

# Function to save extracted text to a JSON file


# Route to home page


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route("/", methods=["GET", "POST"])
def process_image():
    # Execute if request is get
    if request.method == "GET":
        full_filename = 'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename)

    if request.method == "POST":
        file_upload = request.files["file_upload"]
        file_name = file_upload.filename
        file_extension = os.path.splitext(file_name)[1].lower()

        if file_extension in [".jpg", ".jpeg", ".png", ".gif", ".pdf"]:
            # Extract text from image
            text = extract_text_from_image(file_upload)

            if text:
                return render_template("result.html", full_filename=full_filename, text=text)
            else:
                return "Error extracting text from image"

        # # Save extracted text to CSV or JSON based on user's choice
        # save_option = request.form.get('save_option')

        # if save_option == 'csv':
        #     save_to_csv(extracted_text_list, filename='output.csv')
        # elif save_option == 'json':
        #     save_to_json(extracted_text_list, filename='output.json')

        # # Saving image to display in HTML
        # img = Image.fromarray(image_arr, 'RGB')
        # img.save(os.path.join(app.config['INITIAL_FILE_UPLOAD'], name))


if __name__ == '__main__':
    app.run(debug=False)
