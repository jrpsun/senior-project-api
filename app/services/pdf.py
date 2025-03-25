import fitz
import io
from PIL import Image

class PDFProcessor:
    @staticmethod
    def pdf_to_images(pdf_bytes):
        """ แปลง PDF เป็นภาพจาก bytes """
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        image_bytes_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            
            # แปลง Pixmap เป็น PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # แปลง PIL Image เป็น bytes
            img_bytes_io = io.BytesIO()
            img.save(img_bytes_io, format="PNG")
            img_bytes_io.seek(0)

            image_bytes_list.append(img_bytes_io.getvalue())  # เพิ่ม bytes เข้า list

        pdf_document.close()
        return image_bytes_list  # คืนค่าเป็น list ของ bytes