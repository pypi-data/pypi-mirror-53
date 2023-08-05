from django.apps import apps as django_apps
from django.conf import settings as django_settings


ALLOWS_LOOPS = getattr(django_settings, 'EMAIL_TEMPLATE_ALLOW_LOOPS', False)


def get_email_template_model():
    from emailtemplates.models import EmailTemplate
    if getattr(django_settings, 'EMAIL_TEMPLATE_MODEL', False):
        return django_apps.get_model(django_settings.EMAIL_TEMPLATE_MODEL, require_ready=False)
    return EmailTemplate


def get_email_template_settings_model():
    from emailtemplates.models import EmailTemplateSettings
    if getattr(django_settings, 'EMAIL_TEMPLATE_SETTINGS_MODEL', False):
        return django_apps.get_model(django_settings.EMAIL_TEMPLATE_SETTINGS_MODEL, require_ready=False)
    return EmailTemplateSettings
