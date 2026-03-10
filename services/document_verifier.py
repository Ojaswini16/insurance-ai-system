import cv2
import pytesseract

def verify_document(path):

    img=cv2.imread(path)

    text=pytesseract.image_to_string(img)

    if "hospital" in text.lower():
        return "Valid medical document"

    return "Document requires verification"