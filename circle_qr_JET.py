import pandas as pd
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

# НАСТРОЙКИ
EXCEL_FILE = "data.xlsx"
OUTPUT_PDF = "qr_codes.pdf"

# Размер круга
CIRCLE_DIAMETER = 29 * mm
CIRCLE_RADIUS = CIRCLE_DIAMETER / 2

# Размер QR
QR_SIZE = 20 * mm

# Отступы страницы
MARGIN_X = 6 * mm
MARGIN_Y = 6 * mm

# Расстояния между кругами
GAP_X = 8 * mm
GAP_Y = 7 * mm

# Размер блока
BLOCK_WIDTH = CIRCLE_DIAMETER
BLOCK_HEIGHT = CIRCLE_DIAMETER

# ЧТЕНИЕ EXCEL
df = pd.read_excel(EXCEL_FILE, header=None, dtype=str)

# СОЗДАНИЕ PDF
c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)

page_width, page_height = A4

x = MARGIN_X
y = page_height - MARGIN_Y - BLOCK_HEIGHT

# ГЕНЕРАЦИЯ
for index, row in df.iterrows():

    number = str(row[0])
    link = str(row[1])

    # Генерация QR

    qr = qrcode.make(link)

    qr_filename = f"qr_temp_{index}.png"
    qr.save(qr_filename)

    # КРУГЛАЯ РАМКА
    center_x = x + CIRCLE_RADIUS
    center_y = y + CIRCLE_RADIUS

    c.circle(
        center_x,
        center_y,
        CIRCLE_RADIUS,
        stroke=1,
        fill=0
    )

    # QR ПО ЦЕНТРУ
    qr_x = center_x - QR_SIZE / 2
    qr_y = center_y - QR_SIZE / 2

    c.drawImage(
        qr_filename,
        qr_x,
        qr_y,
        QR_SIZE,
        QR_SIZE
    )

    # ТЕКСТ
    c.setFont("Helvetica-Bold", 8)

    # JET сверху между QR и кругом
    jet_y = center_y + (QR_SIZE / 2)

    c.drawCentredString(
        center_x,
        jet_y,
        "JET"
    )

    # Номер снизу между QR и кругом
    number_y = center_y - (QR_SIZE / 2) - 1.8 * mm

    c.drawCentredString(
        center_x,
        number_y,
        number
    )

    # УДАЛЕНИЕ ВРЕМЕННОГО PNG
    if os.path.exists(qr_filename):
        os.remove(qr_filename)

    # СМЕЩЕНИЕ
    x += BLOCK_WIDTH + GAP_X

    # Новая строка
    if x + BLOCK_WIDTH > page_width:
        x = MARGIN_X
        y -= BLOCK_HEIGHT + GAP_Y

    # Новая страница
    if y < MARGIN_Y:
        c.showPage()
        x = MARGIN_X
        y = page_height - MARGIN_Y - BLOCK_HEIGHT

# СОХРАНЕНИЕ PDF

c.save()

print("PDF успешно создан:", OUTPUT_PDF)

