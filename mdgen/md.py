"""import os
import pdfkit
import markdown2


def markdown_to_pdf(input_file, output_file):
    # Read Markdown file content
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_content)

    # Write HTML to a temporary file
    temp_html_file = 'temp.html'
    with open(temp_html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Convert HTML to PDF
    pdfkit.from_file(temp_html_file, output_file)

    # Remove temporary HTML file
    os.remove(temp_html_file)

    input_file = 'outputboss.txt'
    output_file = 'output.pdf'

markdown_to_pdf(input_file, output_file)
"""

import mistune
import pdfkit


#config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
def markdown_to_pdf(input_file, output_file):
    # Read Markdown file content
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
        html = mistune.html(markdown_content)
        pdfkit.from_string(html, output_file,css="theme.css")

        # Remove temporary HTML file



markdown_to_pdf("outputboss.txt", "output.pdf")