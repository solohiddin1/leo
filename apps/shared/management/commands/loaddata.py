import os
import json
from django.core.management import call_command
from modeltranslation.management.commands.loaddata import Command as ModelTranslationLoadDataCommand


class Command(ModelTranslationLoadDataCommand):
    help = "Custom loaddata that supports both standard fixtures and usta dumpdata (dump.json)."

    def handle(self, *fixture_labels, **options):
        usta_labels = []
        regular_labels = []

        for label in fixture_labels:
            is_usta = False
            if label.endswith("dump.json") or "dump.json" in label:
                is_usta = True
            elif os.path.isfile(label):
                try:
                    with open(label, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        model_names = {
                            x.get("model") for x in data[:50] if isinstance(x, dict)
                        }
                        if "user.telegramuser" in model_names or "product.instruction" in model_names:
                            is_usta = True
                except Exception:
                    pass

            if is_usta:
                usta_labels.append(label)
            else:
                regular_labels.append(label)

        for usta_file in usta_labels:
            self.stdout.write(
                f"Detected usta dumpdata file '{usta_file}'. Loading via migrate_from_usta..."
            )
            call_command("migrate_from_usta", usta_file)

        if regular_labels:
            return super().handle(*regular_labels, **options)
        return None
