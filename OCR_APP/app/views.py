# Important imports
from app import app
from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import cv2
import pytesseract
import string
import random
import os
import csv
import json


# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

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

# Route to home page


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/", methods=["GET", "POST"])
def process_image():
    # Execute if request is get
    if request.method == "GET":
        full_filename = 'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename)

    if request.method == "POST":
        image_upload = request.files['image_upload']
        imagename = image_upload.filename
        image = Image.open(image_upload)

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

        # Save extracted text to CSV or JSON based on user's choice
        save_option = request.form.get('save_option')

        if save_option == 'csv':
            save_to_csv(extracted_text_list, filename='output.csv')
        elif save_option == 'json':
            save_to_json(extracted_text_list, filename='output.json')

        # Saving image to display in HTML
        img = Image.fromarray(image_arr, 'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

        # Returning template, filename, extracted text
        return render_template('index.html', full_filename=full_filename, text=extracted_text_list)

        # Main function
if __name__ == '__main__':
    app.run(debug=True)
