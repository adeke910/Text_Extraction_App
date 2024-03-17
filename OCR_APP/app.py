from flask import Flask, render_template, request, jsonify
import os
import csv
import json
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

# # Adding path to config
app.config['INITIAL_FILE_UPLOAD'] = 'static/uploads'

# Function to extract text from an image using EdenAI

url = "https://api.edenai.run/v2/ocr/ocr"

# Eden AI API key
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmIxNTFkM2QtMWM1Mi00MjI2LWJlZjctZmQ5MDM4ZDhiYWFkIiwidHlwZSI6ImFwaV90b2tlbiJ9.opM4_wAVP84SYg_15CRksv0XMNNYGwogSRsHWKa2jsM"

# Function to extract text from an image using Eden AI OCR API


def extract_text_from_image(document_file):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmIxNTFkM2QtMWM1Mi00MjI2LWJlZjctZmQ5MDM4ZDhiYWFkIiwidHlwZSI6ImFwaV90b2tlbiJ9.opM4_wAVP84SYg_15CRksv0XMNNYGwogSRsHWKa2jsM",
    }

    data = {
        "fallback_providers": "",
        "providers": ["google"],
        "language": "en"
    }

    uploads_folder_path = os.path.join(os.getcwd(), 'static')
    image_file_path = os.path.join(uploads_folder_path, 'uploads/test.png')

    files = {"file": open(image_file_path, 'rb')}

    response = requests.post(
        url, data=data, files=files, headers=headers)
    result = json.loads(response.text)
    print(result["google"]["text"])

    return result

# Function to save extracted text to a CSV file


def save_to_csv(data, filename='output.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Text'])
        csv_writer.writerows([[text] for text in data])


# Route to home page

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
                return jsonify({'full_filename': file_name, 'text': text})
            # render_template("index.html", full_filename=file_name, text=text)
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
