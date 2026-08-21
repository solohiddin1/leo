from django.utils.html import format_html


def image_preview(self, obj):
    image = obj.image_compressed or obj.image
    if not image:
        return "-"
    return format_html(
        '<img src="{}" style="max-height:150px; max-width:150px; object-fit:cover;" />',
        image.url,
    )

def image_preview_for_product(self, obj):
    first_image = obj.images.first()
    if not first_image:
        return "-"

    # Use compressed image if available, fallback to original
    image_file = first_image.image_compressed or first_image.image
    return format_html(
        '<img src="{}" style="max-height:150px; max-width:150px; object-fit:cover;" />',
        image_file.url,
    )
