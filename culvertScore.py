import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

textPath = "Images/testImage.png"
img = cv2.imread(textPath)
text = pytesseract.image_to_string(img)
print(text)