from django import apps


class AppConfig(apps.AppConfig):
    name = 'django_saml2_auth_signout_redirect'

    def ready(self):
        # import plugins
        # noinspection PyUnresolvedReferences
        from . import plugins
