import easyocr
import cv2

# Ścieżka do zdjęcia
image_path = 'IMG_5818.jpeg'

# Wczytaj obraz (opcjonalnie do podglądu / przetwarzania)
image = cv2.imread(image_path)

# Inicjalizacja czytnika EasyOCR (['en'] = język angielski, można dodać 'pl' dla polskiego)
reader = easyocr.Reader(['en', 'pl'], gpu=False)  # gpu=True jeśli masz GPU

# Rozpoznanie tekstu
results = reader.readtext(image_path)

# Wyświetlenie wyników
for (bbox, text, prob) in results:
    print(f"Tekst: {text} | Pewność: {prob:.2f}")
    # bbox = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    print(f"Bounding box: {bbox}")

# Opcjonalnie: wyświetlenie obrazu z zaznaczonym tekstem
for (bbox, text, prob) in results:
    (tl, tr, br, bl) = bbox
    top_left = (int(tl[0]), int(tl[1]))
    bottom_right = (int(br[0]), int(br[1]))
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, text, (int(tl[0]), int(tl[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

cv2.imshow("OCR Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
