from django.apps import AppConfig


class ExpensenseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expensense'

    def ready(self):
        from .models import Category
        Category.create_default_categories()
        import expensense.signals



