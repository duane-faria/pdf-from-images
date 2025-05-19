import os
import img2pdf
from PIL import Image, ImageDraw, ImageFont

images_path = "/mnt/c/Users/df/Downloads/prints-mae"
pdf_path = f"{images_path}/pdf.pdf"

groups = {}

for filename in os.listdir(images_path):
    key = filename[0]
    if key not in groups:
        groups[key] = []
    groups[key].append(filename)

print(sorted(groups["6"]))

pdf_bytes = img2pdf.convert(
    [os.path.join(images_path, filename) for filename in groups["6"]]
)

with open(pdf_path, "wb") as f:
    f.write(pdf_bytes)

print("Successfully made pdf file")



# def extract_date(filename):
#     try:
#         # Exemplo: '6 Ano A 06_05_2025.png' → procura '06_05_2025'
#         parts = filename.split()
#         for part in parts:
#             if "_" in part and len(part.split("_")) == 3:
#                 return datetime.strptime(part, "%d_%m_%Y")
#     except Exception:
#         pass
#     # Se não achar uma data válida, retorna uma data mínima para não quebrar o sort
#     return datetime.min

# # Ordena os arquivos do grupo '6' pela data no nome
# image_files = sorted(groups["6"], key=extract_date)




def create_separator_page(message, output_path):
    # A4 in pixels at 300 DPI
    dpi = 300
    a4_width_px = int(210 / 25.4 * dpi)
    a4_height_px = int(297 / 25.4 * dpi)

    img = Image.new("RGB", (a4_width_px, a4_height_px), color="white")
    draw = ImageDraw.Draw(img)

    # Optional: adjust font path as needed
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(message, font=font)
    position = ((a4_width_px - text_width) // 2, (a4_height_px - text_height) // 2)
    draw.text(position, message, fill="black", font=font)

    img.save(output_path, dpi=(dpi, dpi))