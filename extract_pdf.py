import fitz  # PyMuPDF
import os

pdf_path = "포트폴리오_김영훈.pdf"
output_dir = "extracted_pdf_content"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

doc = fitz.open(pdf_path)

full_text = []

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text("text")
    full_text.append(f"--- Page {page_num + 1} ---\n{text}")
    
    # Extract images
    image_list = page.get_images(full=True)
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"image_p{page_num+1}_{img_index}.{image_ext}"
        with open(os.path.join(output_dir, image_filename), "wb") as image_file:
            image_file.write(image_bytes)

with open(os.path.join(output_dir, "extracted_text.txt"), "w", encoding="utf-8") as text_file:
    text_file.write("\n".join(full_text))

print("Extraction complete. Text and images saved to", output_dir)
