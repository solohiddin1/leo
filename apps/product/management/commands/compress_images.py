import logging

from django.core.management.base import BaseCommand

from apps.product.models import Category, Image, SubCategory
from apps.shared.models import Banner
from apps.shared.utils.compress import compress_image

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Compresses images (Category, SubCategory, Image, Banner) to WebP format. "
        "Safe to run multiple times: skips images that are already compressed."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-compress even if image_compressed already exists on disk",
        )
        parser.add_argument(
            "--model",
            choices=["all", "image", "category", "subcategory", "banner"],
            default="all",
            help="Specify which model to process (default: all)",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Limit number of images processed per model (0 = process all)",
        )

    def handle(self, *args, **options):
        force = options["force"]
        model_choice = options["model"]
        limit = options["limit"]

        models_to_process = []
        if model_choice in ("all", "category"):
            models_to_process.append(("Category", Category, "image", "image_compressed"))
        if model_choice in ("all", "subcategory"):
            models_to_process.append(("SubCategory", SubCategory, "image", "image_compressed"))
        if model_choice in ("all", "image"):
            models_to_process.append(("Product Image", Image, "image", "image_compressed"))
        if model_choice in ("all", "banner"):
            models_to_process.append(("Banner", Banner, "image", "image_compressed"))

        total_compressed = 0
        total_skipped = 0
        total_missing = 0
        total_errors = 0

        for label, model_class, src_field, dest_field in models_to_process:
            self.stdout.write(self.style.NOTICE(f"\nProcessing {label}..."))
            qs = model_class.objects.all().order_by("pk")
            if limit > 0:
                qs = qs[:limit]

            compressed_count = 0
            skipped_count = 0
            missing_count = 0
            error_count = 0

            for obj in qs.iterator():
                src = getattr(obj, src_field)
                if not src or not src.name:
                    skipped_count += 1
                    continue

                dest = getattr(obj, dest_field)
                # Check if already compressed
                if not force and dest and dest.name:
                    try:
                        if dest.storage.exists(dest.name):
                            skipped_count += 1
                            continue
                    except Exception:
                        pass

                # Check if source file exists on disk
                try:
                    if not src.storage.exists(src.name):
                        missing_count += 1
                        continue
                except Exception:
                    missing_count += 1
                    continue

                try:
                    with src.open("rb"):
                        compressed_file = compress_image(
                            src,
                            sizes=None,
                            format="WEBP",
                            quality=82,
                            keep_dimensions=True,
                        )
                    dest.save(compressed_file.name, compressed_file, save=False)
                    model_class.objects.filter(pk=obj.pk).update(**{dest_field: dest.name})
                    compressed_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"  Failed {label} #{obj.pk} ({src.name}): {e}")
                    )
                    logger.exception(f"Error compressing {label} #{obj.pk}")
                    error_count += 1

            self.stdout.write(
                f"  {label} summary: "
                f"{compressed_count} compressed, "
                f"{skipped_count} skipped (already compressed or empty), "
                f"{missing_count} missing from disk, "
                f"{error_count} errors"
            )

            total_compressed += compressed_count
            total_skipped += skipped_count
            total_missing += missing_count
            total_errors += error_count

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTotal: {total_compressed} compressed, "
                f"{total_skipped} skipped, "
                f"{total_missing} missing, "
                f"{total_errors} errors."
            )
        )
