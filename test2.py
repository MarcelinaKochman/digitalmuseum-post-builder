import cv2
from PIL import Image
import pytesseract

# Wczytanie obrazu przez OpenCV
cv_image = cv2.imread("IMG_5818.jpg")

# Konwersja do RGB (OpenCV używa BGR)
cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

# Konwersja na PIL Image
pil_image = Image.fromarray(cv_image)

# OCR
text = pytesseract.image_to_string(pil_image)
print(text)
