from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.shared.middleware.middleware import get_logger
from apps.shared.utils.compress import compress_image

from .models import Category, Image, SubCategory

logger = get_logger()


def _compress_product_image(instance: Image) -> None:
    try:
        import os

        if not instance.image:
            return

        image_desktop = compress_image(
            instance.image,
            sizes=None,
            format="WEBP",
            quality=82,
            keep_dimensions=True,
        )

        instance.image_compressed.save(image_desktop.name, image_desktop, save=False)
        Image.objects.filter(pk=instance.pk).update(
            image_compressed=instance.image_compressed,
        )

        old_paths = {
            'original': getattr(instance, '_old_image', None),
            'compressed': getattr(instance, '_old_image_compressed', None),
        }

        for img_type, old_path in old_paths.items():
            if old_path and os.path.exists(old_path):
                try:
                    os.remove(old_path)
                    logger.info(f"🗑️  Deleted old {img_type} image: {old_path}")
                except Exception as delete_error:
                    logger.warning(f"⚠️  Failed to delete old {img_type} image: {delete_error}")

        logger.info(f"✅ Image #{instance.pk} compressed successfully")
    except Exception as e:
        logger.exception(f"❌ Error compressing Image #{instance.pk}: {e}")


@receiver(pre_save, sender=Image)
def track_product_image_changes(sender, instance, **kwargs):
    print(f"Tracking changes for Image #{instance.pk}")

    if not instance.pk:
        instance._image_changed = bool(instance.image)
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        instance._image_changed = old_instance.image != instance.image

        if instance._image_changed:
            instance._old_image = old_instance.image.path if old_instance.image else None
            instance._old_image_compressed = old_instance.image_compressed.path if old_instance.image_compressed else None
    except sender.DoesNotExist:
        instance._image_changed = bool(instance.image)


@receiver(post_save, sender=Image)
def compress_product_image_after_save(sender, instance, created, **kwargs):
    if not instance.image:
        return

    should_compress = created or getattr(instance, '_image_changed', False)
    if not should_compress:
        return

    transaction.on_commit(lambda: _compress_product_image(instance))


def _compress_category_image(instance, src_field: str, dest_field: str) -> None:
    try:
        import os

        src = getattr(instance, src_field)
        if not src:
            return

        compressed = compress_image(
            src, sizes=None, format="WEBP", quality=82, keep_dimensions=True
        )

        dest = getattr(instance, dest_field)
        dest.save(compressed.name, compressed, save=False)

        instance.__class__.objects.filter(pk=instance.pk).update(**{dest_field: dest})

        old_path = getattr(instance, f'_old_{dest_field}_path', None)
        if old_path and os.path.exists(str(old_path)):
            try:
                os.remove(str(old_path))
                logger.info(f"🗑️  Deleted old compressed image: {old_path}")
            except OSError as delete_error:
                logger.warning(f"⚠️  Failed to delete old compressed image: {delete_error}")

        cls_name = instance.__class__.__name__
        logger.info(f"✅ {cls_name} #{instance.pk} {src_field} compressed successfully")
    except Exception:
        cls_name = instance.__class__.__name__
        logger.exception(f"❌ Error compressing {cls_name} #{instance.pk} {src_field}")


@receiver(pre_save, sender=Category)
def track_category_image_changes(sender, instance, **kwargs):
    if not instance.pk:
        instance._image_changed = bool(instance.image)
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        instance._image_changed = old_instance.image != instance.image
        if instance._image_changed:
            instance._old_image_compressed_path = (
                old_instance.image_compressed.path if old_instance.image_compressed else None
            )
    except sender.DoesNotExist:
        instance._image_changed = bool(instance.image)


@receiver(post_save, sender=Category)
def compress_category_image_after_save(sender, instance, created, **kwargs):
    if not instance.image:
        return

    should_compress = created or getattr(instance, '_image_changed', False)
    if not should_compress:
        return

    transaction.on_commit(lambda: _compress_category_image(instance, 'image', 'image_compressed'))


@receiver(pre_save, sender=SubCategory)
def track_subcategory_image_changes(sender, instance, **kwargs):
    if not instance.pk:
        instance._image_changed = bool(instance.image)
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        instance._image_changed = old_instance.image != instance.image
        if instance._image_changed:
            instance._old_image_compressed_path = (
                old_instance.image_compressed.path if old_instance.image_compressed else None
            )
    except sender.DoesNotExist:
        instance._image_changed = bool(instance.image)


@receiver(post_save, sender=SubCategory)
def compress_subcategory_image_after_save(sender, instance, created, **kwargs):
    if not instance.image:
        return

    should_compress = created or getattr(instance, '_image_changed', False)
    if not should_compress:
        return

    transaction.on_commit(lambda: _compress_category_image(instance, 'image', 'image_compressed'))
