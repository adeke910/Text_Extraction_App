# Important imports
# from app import app
from flask import Flask, render_template, request, jsonify, app
from PIL import Image
import numpy as np
import cv2
import pytesseract
import string
import random
import os
import csv
import json
import fitz  # PyMuPDF
# from utils import extract_text_from_image, remove_characters, save_to_csv, save_to_json


# Adding path to config
app.config['INITIAL_FILE_UPLOAD'] = 'app/static/uploads'

# Function to extract text from an image using Tesseract


def extract_text_from_image(image):
    custom_config = r'-l eng --oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

# Function to remove specified characters from a string


def remove_characters(text, characters):
    for character in characters:
        text = text.replace(character, "")
    return text

# Function to save extracted text to a CSV file


def save_to_csv(data, filename='output.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Text'])
        csv_writer.writerows([[text] for text in data])

# Function to save extracted text to a JSON file


def save_to_json(data, filename='output.json'):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)


def extract_text_from_pdf(pdf_file):
    text = ''
    try:
        pdf_document = fitz.open(pdf_file)
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()
        pdf_document.close()
    except Exception as e:
        return f'Error extracting text from PDF: {str(e)}'
    return text

# Route to home page


@app.route("/", methods=["GET", "POST"])
def process_image():
    # Execute if request is get
    if request.method == "GET":
        full_filename = 'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename)

    if request.method == "POST":
        file_upload = request.files['file_upload']
        file_name = file_upload.filename

        # check the file extension
        _, file_extension = os.path.splittext(file_name)

        if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            # process image file
            image = Image.open(file_upload)

            # Converting image to array
            image_arr = np.array(image.convert('RGB'))

            # Converting image to grayscale
            gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
            # Converting image back to RGB
            image = Image.fromarray(gray_img_arr)

            # Printing lowercase
            letters = string.ascii_lowercase

            # Generating unique image name for dynamic image display
            name = ''.join(random.choice(letters) for i in range(10)) + '.png'
            full_filename = 'uploads/' + name

            # Extracting text from image
            text = extract_text_from_image(image)

            # Remove specified symbols
            characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~"
            cleaned_text = remove_characters(text, characters_to_remove)

            # Converting string into a list to display extracted text in separate lines
            extracted_text_list = cleaned_text.split("\n")

        elif file_extension.lower == '.pdf':
            # process PDF file
            extracted_text_list = extract_text_from_pdf(file_upload)

        # Save extracted text to CSV or JSON based on user's choice
        save_option = request.form.get('save_option')

        if save_option == 'csv':
            save_to_csv(extracted_text_list, filename='output.csv')
        elif save_option == 'json':
            save_to_json(extracted_text_list, filename='output.json')

        # Saving image to display in HTML
        img = Image.fromarray(image_arr, 'RGB')
        img.save(os.path.join(app.static['INITIAL_FILE_UPLOAD'], name))

        # Returning template, filename, extracted text
        return render_template('index.html', full_filename=full_filename, text=extracted_text_list)

        # Main function
if __name__ == '__main__':
    app.run(debug=True)
