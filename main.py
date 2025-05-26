import os
import img2pdf
from datetime import datetime

folder_path = "/mnt/c/Users/df/Downloads/prints-mae"
PDF_OUTPUT = "final.pdf"
groups = {}


def remove_partial_pdfs():
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf") and filename != PDF_OUTPUT:
            os.remove(f"{folder_path}/{filename}")


def get_school_class_name_from_screenshot(name: str) -> str:
    splited = name.split(" ")
    return " ".join(splited[0 : len(splited) - 1])


def extract_date(filename):
    try:
        # Exemplo: '6 Ano A 06_05_2025.png' → procura '06_05_2025'
        parts = filename.replace(".png", "").split()
        for part in parts:
            if "_" in part and len(part.split("_")) == 3:
                return datetime.strptime(part, "%d_%m_%Y")
    except Exception:
        pass
    # Se não achar uma data válida, retorna uma data mínima para não quebrar o sort
    return datetime.min


for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        os.remove(f"{folder_path}/{filename}")
    if filename.endswith((".png", ".jpg")):
        key = get_school_class_name_from_screenshot(filename)
        if key not in groups:
            groups[key] = []
        groups[key].append(filename)


def create_divider_pdf_page(page_title: str):
    import pdfkit

    html_content = f"""
    <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body style="display: flex; align-items:center; justify-content:center; font-size: 60px">
            <h1 style="text-align:center">{page_title}</h1>
        </body>
    </html>
    """
    pdf_name = f"{folder_path}/{page_title}-divider-page.pdf"
    pdfkit.from_string(html_content, pdf_name)
    return pdf_name


def create_pdf_from_images(image_paths, pdf_name):
    pdf_bytes = img2pdf.convert(
        [os.path.join(folder_path, filename) for filename in image_paths]
    )
    pdf_path = f"{folder_path}/{pdf_name}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    return pdf_path


def merge_pdfs(pdf_files):
    from PyPDF2 import PdfMerger

    merger = PdfMerger()
    for pdf in pdf_files:
        print(pdf)
        merger.append(f"{pdf}")

    merger.write(f"{folder_path}/{PDF_OUTPUT}")
    # merger.close()


all_pdfs = []
for group_key in groups.keys():
    screeshot_pdf_name = get_school_class_name_from_screenshot(groups[group_key][0])
    divider_page_pdf_name = create_divider_pdf_page(screeshot_pdf_name)

    created_pdf = create_pdf_from_images(
        sorted(groups[group_key], key=extract_date), screeshot_pdf_name
    )

    all_pdfs.append(divider_page_pdf_name)
    all_pdfs.append(created_pdf)

merge_pdfs(all_pdfs)
remove_partial_pdfs()
