import pandas as pd
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

# НАСТРОЙКИ
EXCEL_FILE = "data.xlsx"
OUTPUT_PDF = "qr_codes.pdf"

QR_SIZE = 21 * mm
MARGIN_X = 6 * mm
MARGIN_Y = 6 * mm
GAP_X = 8 * mm
GAP_Y = 7 * mm

TEXT_HEIGHT = 2       # высота строки текста (для шрифта 8)
TEXT_GAP = 0    # 0 мм между QR и номером
FRAME_PADDING = 3     # отступ рамки

# Читаем Excel
df = pd.read_excel(EXCEL_FILE, header=None)

# Создаём PDF
c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
page_width, page_height = A4

x = MARGIN_X
y = page_height - MARGIN_Y - QR_SIZE

# Размер блока (QR + номер)
BLOCK_HEIGHT = QR_SIZE + TEXT_GAP + TEXT_HEIGHT
BLOCK_WIDTH = QR_SIZE

for index, row in df.iterrows():
    number = str(row[0])
    link = str(row[1])

    # Генерация QR-кода
    qr = qrcode.make(link)
    qr_filename = f"qr_temp_{index}.png"
    qr.save(qr_filename)

    # РАМКА
    FRAME_WIDTH = 24.5 * mm
    FRAME_HEIGHT = 23.5 * mm

    RADIUS = 2 * mm  # радиус скругления

    c.roundRect(
        x + (QR_SIZE - FRAME_WIDTH) / 2,
        y - (FRAME_HEIGHT - QR_SIZE) / 2 - 2,
        FRAME_WIDTH,
        FRAME_HEIGHT,
        radius=RADIUS,
        stroke=1,
        fill=0
    )

    # QR-код
    c.drawImage(qr_filename, x, y, QR_SIZE, QR_SIZE)

    # НОМЕР — сразу под QR с отступом 1 мм
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(
        x + QR_SIZE / 2,
        y - TEXT_GAP - TEXT_HEIGHT,
        number
    )

    os.remove(qr_filename)

    # Смещение по X
    x += QR_SIZE + GAP_X

    if x + QR_SIZE > page_width:
        x = MARGIN_X
        y -= BLOCK_HEIGHT + GAP_Y

    if y < MARGIN_Y:
        c.showPage()
        x = MARGIN_X
        y = page_height - MARGIN_Y - QR_SIZE

c.save()
print("PDF успешно создан:", OUTPUT_PDF)