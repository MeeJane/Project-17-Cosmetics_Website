from django.apps import AppConfig


class GlowifyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "glowify"

    def ready(self):
        import glowify.signals
