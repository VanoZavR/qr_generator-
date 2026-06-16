import os
import pandas as pd
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

EXCEL_FILE = "data.xlsx"
OUTPUT_PDF = "qr_codes.pdf"

# Размер QR
QR_SIZE = 17 * mm

MARGIN_X = 6 * mm
MARGIN_Y = 6 * mm

TEXT_GAP = 1.5 * mm

# Размер рамки
FRAME_WIDTH = 24.2 * mm
FRAME_HEIGHT = 23.2 * mm

RADIUS = 2 * mm  # скругление

# Читаем Excel
df = pd.read_excel(EXCEL_FILE, header=None, dtype=str)

# Создаём PDF
c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
page_width, page_height = A4

# Фиксированная позиция одного QR на странице
x = MARGIN_X
y = page_height - MARGIN_Y - FRAME_HEIGHT

for index, row in df.iterrows():
    number = str(row[0])
    link = str(row[1])

    # Генерация QR-кода
    qr = qrcode.make(link)
    qr_filename = f"qr_temp_{index}.png"
    qr.save(qr_filename)

    # РАМКА
    c.roundRect(
        x,
        y,
        FRAME_WIDTH,
        FRAME_HEIGHT,
        radius=RADIUS,
        stroke=1,
        fill=0
    )

    # Центр рамки
    center_x = x + FRAME_WIDTH / 2

    # Внутренний отступ
    INNER_PADDING = 2 * mm

    # Высота текстовых зон
    TEXT_ZONE = 4 * mm

    # QR по центру рамки
    qr_x = x + (FRAME_WIDTH - QR_SIZE) / 2

    qr_y = (
        y
        + INNER_PADDING
        + TEXT_ZONE
        + (
            FRAME_HEIGHT
            - 2 * INNER_PADDING
            - 2 * TEXT_ZONE
            - QR_SIZE
        ) / 2
    )

    # QR
    c.drawImage(qr_filename, qr_x, qr_y, QR_SIZE, QR_SIZE)

    # Шрифт
    c.setFont("Helvetica-Bold", 8)

    # JET — центр между верхом рамки и QR
    jet_y = qr_y + QR_SIZE + (
            y + FRAME_HEIGHT - (qr_y + QR_SIZE)
    ) / 2 - 3 - (1 * mm)

    c.drawCentredString(
        center_x,
        jet_y,
        "JET"
    )

    # Номер — центр между QR и низом рамки
    number_y = y + (qr_y - y) / 2 - 3 + (1 * mm)

    c.drawCentredString(
        center_x,
        number_y,
        number
    )

    # УДАЛЕНИЕ ВРЕМЕННОГО PNG
    if os.path.exists(qr_filename):
        os.remove(qr_filename)

    # КАЖДЫЙ QR НА НОВОЙ СТРАНИЦЕ
    c.showPage()

c.save()

print("PDF успешно создан:", OUTPUT_PDF)

# Дополнительная проверка удаления PNG
for index in df.index:
    qr_filename = f"qr_temp_{index}.png"

    if os.path.exists(qr_filename):
        os.remove(qr_filename)

print("Временные PNG удалены")