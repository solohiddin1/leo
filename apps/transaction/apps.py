from django.apps import AppConfig


class TransactionConfig(AppConfig):
    name = 'apps.transaction'
    label = 'transaction'

    def ready(self):
        import apps.transaction.signals  # noqa: F401
        try:
            import jazzmin.templatetags.jazzmin as jazzmin_tags
            from django.utils.safestring import mark_safe

            # Save the original function reference
            original_paginator_number = jazzmin_tags.jazzmin_paginator_number

            def safe_jazzmin_paginator_number(change_list, i):
                # Call the original function or replicate the template generation
                # Return mark_safe directly to satisfy Django 4+/5+/6+ strict format_html check
                res = original_paginator_number(change_list, i)
                return mark_safe(res) if isinstance(res, str) else res

            # Override the tag in the Jazzmin module
            jazzmin_tags.jazzmin_paginator_number = safe_jazzmin_paginator_number

        except (ImportError, AttributeError):
            pass