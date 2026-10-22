import os  # noqa: I001
import io
import requests
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.conf import settings

"""for product model"""


def compress_image(
    image_file,
    sizes: tuple | None,
    format: str,
    quality: int,
    keep_dimensions: bool = False,
):
    print(f"Compressing image {image_file.name} in format {format}...")
    img = Image.open(image_file)
    img = ImageOps.exif_transpose(img)

    if sizes and not keep_dimensions:
        output_img = img.resize(sizes, Image.LANCZOS)
        output_size = sizes
    else:
        output_img = img
        output_size = img.size

    if output_img.mode in ("RGBA", "LA") or (output_img.mode == "P" and "transparency" in output_img.info):
        if format.upper() in {"JPEG", "JPG"}:
            output_img = output_img.convert("RGBA")
            background = Image.new("RGBA", output_img.size, (255, 255, 255, 255))
            output_img = Image.alpha_composite(background, output_img).convert("RGB")
        elif format.upper() == "WEBP":
            output_img = output_img.convert("RGBA")
    elif output_img.mode not in {"RGB", "RGBA", "L"}:
        output_img = output_img.convert("RGB")

    buffer = io.BytesIO()
    save_kwargs = {
        "format": format,
        "quality": quality,
        "optimize": True,
    }
    if format.upper() == "WEBP":
        save_kwargs["method"] = 4

    output_img.save(buffer, **save_kwargs)
    ext = format.lower()
    name, _ = os.path.splitext(os.path.basename(image_file.name))
    filename = f"{name}_{output_size[0]}x{output_size[1]}.{ext}"

    return ContentFile(buffer.getvalue(), name=filename)


def send_product_inquiry_telegram(name, phone_number, message, product_data=None):
    TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
    CHAT_ID = settings.CHAT_ID

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    inquiry_text = (
        f"<b>🛒 Yangi Mahsulot So'rovi</b>\n\n"
        f"<b>👤 Ism:</b> {name}\n"
        f"<b>📞 Telefon:</b> {phone_number}\n"
        f"<b>💬 Xabar:</b> {message}\n"
    )

    if product_data:
        inquiry_text += (
            f"\n<b>📦 Mahsulot Ma'lumotlari:</b>\n"
            f"<b>🔹 Nomi:</b> {product_data.get('name')}\n"
            f"<b>🔹 Artikul:</b> {product_data.get('sku')}\n"
            f'<b>🔗 Link:</b> <a href="{product_data.get("url")}">Ko\'rish</a>\n'
        )

    payload = {"chat_id": CHAT_ID, "text": inquiry_text, "parse_mode": "HTML"}
    response = requests.post(url, data=payload)
    return response
