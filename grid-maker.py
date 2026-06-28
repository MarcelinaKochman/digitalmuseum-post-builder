from PIL import Image
import os
import math

# PARAMETRY
folder = "/Users/marcelinakochman/Downloads/Wedding Taboo card coastal cowgirl"
output_folder = os.path.join(folder, "grid")
grid_size = (4, 4)
output_prefix = "grid"

# ZBIERZ I SORTUJ OBRAZKI NUMERYCZNIE
files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))  # sortowanie po liczbie z nazwy pliku
image_paths = [os.path.join(folder, f) for f in files]

# SPRAWDŹ ILE OBRAZÓW
total_images = len(image_paths)
images_per_grid = grid_size[0] * grid_size[1]
num_grids = math.ceil(total_images / images_per_grid)

# USTAL ROZMIAR NA PODSTAWIE 1. OBRAZU
sample_image = Image.open(image_paths[0])
img_width, img_height = sample_image.size

# UTWÓRZ FOLDER WYJŚCIOWY
os.makedirs(output_folder, exist_ok=True)

# GENERUJ GRIDY
for i in range(num_grids):
    grid_img = Image.new("RGBA", (img_width * grid_size[0], img_height * grid_size[1]), (255, 255, 255, 255))

    for j in range(images_per_grid):
        index = i * images_per_grid + j
        if index >= total_images:
            break
        img = Image.open(image_paths[index])
        x = (j % grid_size[0]) * img_width
        y = (j // grid_size[0]) * img_height
        grid_img.paste(img, (x, y))

    output_path = os.path.join(output_folder, f"{output_prefix}_{i + 1}.png")
    grid_img.save(output_path)
    print(f"Zapisano: {output_path}")
