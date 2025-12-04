from django.apps import AppConfig


class ProductsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'productsapp'
    def ready(self):
        # import signals to register them
        import productsapp.signals