from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(content, filename):

    c = canvas.Canvas(filename, pagesize=letter)

    y = 750
    lines = content.split("\n")

    for line in lines:
        c.drawString(40, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    c.save()

    return filename
