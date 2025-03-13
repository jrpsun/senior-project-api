import fitz
import io

class PDFProcessor:
    @staticmethod
    def pdf_to_images(pdf_bytes):
        """ แปลง PDF เป็นภาพจาก bytes """
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        image_bytes_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()

            # บันทึกเป็น byte
            image_bytes = io.BytesIO()
            image_bytes.write(pix.tobytes("png"))
            image_bytes.seek(0)
            image_bytes_list.append(image_bytes)

        pdf_document.close()
        return image_bytes_list
