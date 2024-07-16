import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\phuoc\Documents\Code\PythonProjects\DiscordMapleBot\Tesseract\tesseract.exe'
def clean_string(s):
    cleaned_string = s.replace('.', '_')
    return re.sub(r'[^A-Za-z0-9\s_]', '', cleaned_string)

def get_data(image):
    # Grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    # Perform text extraction
    # Best: 1
    data = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    s = clean_string(data)
    # print(s)
    # result = []
    # lines = s.strip().split('\n')
    # for line in lines:
    #     match = re.search(r'(\w+)\s+(\w+(?: \w+)*)\s+(\d+)\s+(\w+)\s+(\d+)\s+(\d+)', line)
    #     if match:
    #         name, player_class, level, score = match.groups()[:3] + match.groups()[5:]
    #         result.append({
    #             'name': name,
    #             'class': player_class,
    #             'level': level,
    #             'score': score
    #         })
    return s