from PIL import Image, ImageDraw, ImageFont
from st7735 import ST7735
import time

DC_PIN = 24
RST_PIN = 22
CS_PIN = 0
SPI_PORT = 0

disp = ST7735(
    port=SPI_PORT,
    cs=CS_PIN,
    dc=DC_PIN,
    rst=RST_PIN,
    spi_speed_hz=40000000,
    width=160,
    height=80,
    rotation=0
)

def launch_animation(logo_path, text):
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
    for fade in range(0, 256, 32):
        image = Image.new("RGB", (160, 80), "black")
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((48, 48), Image.LANCZOS)
        faded_logo = logo.copy()
        faded_logo.putalpha(int(min(fade, 255)))
        image.paste(faded_logo, ((160-48)//2, 8), faded_logo)
        draw = ImageDraw.Draw(image)
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        y_text = 58
        draw.text(((160-w)//2, y_text), text, font=font, fill=(fade, fade, fade))
        image = image.transpose(Image.ROTATE_180)
        disp.display(image)
        time.sleep(0.08)
    time.sleep(1.5)

launch_animation("Logo.png", "Hi!")
