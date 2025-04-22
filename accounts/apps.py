from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import django.contrib.auth.middleware
        from .middleware import JWTAuthenticationMiddleware

        django.contrib.auth.middleware.AuthenticationMiddleware = JWTAuthenticationMiddleware
