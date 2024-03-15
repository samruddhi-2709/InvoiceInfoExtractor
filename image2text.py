import streamlit as st
import pytesseract
from PIL import Image
import io
import json
import re


# Function to extract text from image using Tesseract OCR
def extract_text(image):
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text


# Function to extract date and total amount from text
def extract_date_and_total(text):
    # Define regular expression to match dates in the format "DD-month-YY"
    date_regex = r'\b(\d{1,2}-[A-Za-z]{3}-\d{2})\b'
    date_matches = re.findall(date_regex, text)

    # Define regular expression pattern to match total line
    total_regex = r'Total\s+\d+\s+nos\.\s+.*?\s+([0-9,]+(?:\.\d{2})?)'
    total_match = re.search(total_regex, text, re.IGNORECASE)

    # Extract amount from the total match
    total_amount = None
    if total_match:
        total_amount_str = total_match.group(1)
        # Remove commas and convert to float
        total_amount = float(total_amount_str.replace(',', ''))

    return date_matches, total_amount


# Main Streamlit app
def main():
    st.title("Invoice Info Extractor")

    # Upload image file
    image_file = st.file_uploader("Upload Invoice Image", type=["jpg", "png"])

    if image_file is not None:
        image = Image.open(image_file)

        # Perform OCR to extract text
        extracted_text = extract_text(image)

        # Extract date and total amount from text
        dates, total_amount = extract_date_and_total(extracted_text)

        # Convert to JSON
        invoice_data = {
            "dates": dates,
            "total_amount": total_amount
        }
        invoice_json = json.dumps(invoice_data, indent=4)

        # Display extracted data
        st.header("Extracted Invoice Data:")
        st.json(invoice_json)


# Run the app
if __name__ == "__main__":
    main()