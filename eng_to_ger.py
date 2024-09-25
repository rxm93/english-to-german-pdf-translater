import PyPDF2
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to translate text using Google Translator
def translate_text(text, src='en', dest='de'):
    translator = Translator()
    translated = translator.translate(text, src=src, dest=dest)
    return translated.text

# Function to create a PDF with translated text
def create_pdf_with_translated_text(output_pdf_path, translated_text):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    text_margin = 40
    y = height - 40
    font_size = 12
    line_spacing = 15
    
    # Set font and size
    c.setFont("Helvetica", font_size)

    # Split text into lines that fit the page width
    lines = translated_text.split('\n')
    
    for line in lines:
        # Break line into smaller lines if it exceeds the page width
        split_lines = simpleSplit(line, "Helvetica", font_size, width - 2 * text_margin)
        for split_line in split_lines:
            if y < text_margin:  # Start a new page if out of space
                c.showPage()
                c.setFont("Helvetica", font_size)
                y = height - 40
            c.drawString(text_margin, y, split_line)
            y -= line_spacing

    # Save the PDF
    c.save()

# Main function to handle the translation process
def translate_pdf(input_pdf_path, output_pdf_path):
    # Extract text from the input PDF
    english_text = extract_text_from_pdf(input_pdf_path)
    
    # Translate the extracted text
    german_text = translate_text(english_text, src='en', dest='de')
    
    # Create a new PDF with the translated text
    create_pdf_with_translated_text(output_pdf_path, german_text)
    print(f'Translated PDF created: {output_pdf_path}')

# Usage example
input_pdf = '/content/input_file.pdf'  # Path to the input English PDF
output_pdf = '/content/output_german.pdf'  # Path to the output German PDF

translate_pdf(input_pdf, output_pdf)
