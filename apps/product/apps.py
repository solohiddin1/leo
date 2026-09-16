from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = "apps.product"
    label = "product"

    def ready(self):
        import apps.product.signals
