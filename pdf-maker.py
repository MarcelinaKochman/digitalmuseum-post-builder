from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

# PARAMETRY
grid_folder = "/Users/marcelinakochman/Downloads/Wedding Taboo card coastal cowgirl/grid"
output_pdf = "output.pdf"
margin_cm = 1  # marginesy z każdej strony
a4_width, a4_height = A4
usable_width = a4_width - 2 * margin_cm * cm
usable_height = a4_height - 2 * margin_cm * cm

# SORTUJEMY OBRAZY
files = [f for f in os.listdir(grid_folder) if f.lower().endswith(".png")]
files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
grid_paths = [os.path.join(grid_folder, f) for f in files]

# TWORZENIE PDF
c = canvas.Canvas(output_pdf, pagesize=A4)

for path in grid_paths:
    img = ImageReader(path)
    img_width, img_height = img.getSize()

    # Oblicz współczynnik skalowania do dostępnego obszaru (proporcjonalnie)
    scale = min(usable_width / img_width, usable_height / img_height)
    display_width = img_width * scale
    display_height = img_height * scale

    # Pozycjonowanie (wyśrodkowanie)
    x = (a4_width - display_width) / 2
    y = (a4_height - display_height) / 2

    c.drawImage(img, x, y, width=display_width, height=display_height, preserveAspectRatio=True, mask='auto')
    c.showPage()

c.save()
print(f"✅ Zapisano PDF bez utraty jakości: {output_pdf}")
