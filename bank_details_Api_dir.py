from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
from paddleocr import PaddleOCR
from PIL import Image, ImageEnhance
import numpy as np
import re
import gc
app = Flask(__name__)

# Initialize PaddleOCR
#ocr = PaddleOCR(use_angle_cls=True, lang='en')

@app.route('/compare-bank-details1', methods=['POST'])
def compare_bank_details1():
    try:
        # Clean up old memory (garbage collection)
        gc.collect()

        # Initialize PaddleOCR inside the route to avoid issues with persistence between requests
        ocr = PaddleOCR(use_angle_cls=True, lang='en')

        # Validate if the file is in the request
        if 'file' not in request.files:
            return jsonify({'error': 'File is missing'}), 400

        # Retrieve the uploaded file directly from the request
        file = request.files['file']

        # Read the PDF file as bytes
        pdf_bytes = file.read()

        # Convert the PDF bytes to images
        images = convert_from_bytes(pdf_bytes, dpi=400)

        # Extract text from images using PaddleOCR
        all_text = ""
        for page_num, image in enumerate(images, start=1):
            # Preprocess the image (grayscale, increase contrast)
            print(f"Processing page {page_num}...")
            image = image.convert("L")  # Convert to grayscale
            enhancer = ImageEnhance.Contrast(image)  # Increase contrast
            image = enhancer.enhance(2.0)

            # Convert PIL image to NumPy array for PaddleOCR
            image_np = np.array(image)

            # Perform OCR
            result = ocr.ocr(image_np, cls=True)
            if result and isinstance(result[0], list) and len(result[0]) > 0:
                for line in result[0]:
                    all_text += line[1][0] + "\n"

            # Free up memory after processing each page
            del image, image_np, result
            gc.collect()        

        # Regular expression patterns
        ifsc_pattern = r"(IFS|IFSC|IFS CODE|IFS Code|IFS CODE|IFS COJE|IFSC CODE)\s*[:\-]?\s*([A-Z]{4}0[A-Z0-9]{6})"
        ac_no_pattern = r"(A/c\s*No\.|A/c\.?\s*No\.|Account Number)\s*[:\-]?\s*(\d{9,18})"
        patient_name_pattern = r"(Patient Name|PT.NAME|Name of Patient|Pateint Name|patient name|Patient|Name)\s*[:\-]?\s*(.+)"
        #patient_name_pattern = r"(PT\.NAME|Name of Patient|Patient Name|patient name|Patient)\s*[:\-]?\s*(.*)"


        fourteen_or_sixteen_digit_pattern = r"\b(\d{11}|\d{12}|\d{13}|\d{14}|\d{15}|\d{16})\b"
        #fourteen_or_sixteen_digit_pattern = r"\b(?!0{11}|0{14}|0{15}|0{16})\d{11}|\d{14}|\d{15}|\d{16}\b"



        # Extract data using regex
        ifsc_match = re.search(ifsc_pattern, all_text, re.IGNORECASE)
        ac_no_match = re.search(ac_no_pattern, all_text, re.IGNORECASE)
        patient_name_match = re.search(patient_name_pattern, all_text, re.IGNORECASE)
        fourteen_or_sixteen_digit_matches = re.findall(fourteen_or_sixteen_digit_pattern, all_text)

        # Extracted values
        ifsc_code_value = ifsc_match.group(2) if ifsc_match else "Not Found"
        ac_no_value = ac_no_match.group(2) if ac_no_match else "Not Found"
        patient_name_value = patient_name_match.group(2).strip() if patient_name_match else "Not Found"
        fourteen_or_sixteen_digit_value = (
            fourteen_or_sixteen_digit_matches[0] if fourteen_or_sixteen_digit_matches else "Not Found"
        )

        # Prepare the extracted data for response
        extracted_data = {
            'name': patient_name_value,
            'account_number': fourteen_or_sixteen_digit_value,
            'ifs_code': ifsc_code_value
        }
        print("extracted_data from Docker_server ====>>", extracted_data)

        # Return extracted data as JSON response
        return jsonify(extracted_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8080, debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)


