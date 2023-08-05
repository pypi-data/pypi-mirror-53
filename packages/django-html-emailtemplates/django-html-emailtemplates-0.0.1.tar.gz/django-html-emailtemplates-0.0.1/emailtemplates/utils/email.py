from django.conf import settings as django_settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.template import Context, Template
from premailer import transform


def render_string_email_template(template_string, context={}):
    if isinstance(template_string, str) or isinstance(template_string, unicode):
        if '{% load static %}' not in template_string:
            template_string = '{% load static %}' + template_string
    context.update({
        'protocol': 'http',
        'domain': Site.objects.get_current().domain
    })
    t = Template(template_string)
    return t.render(Context(context))


def extend_email_template(template, context={}):
    t = get_template(template)
    http = 'https'
    if django_settings.DEBUG:
        http = 'http'
    base_url = '%s://%s' % (http, Site.objects.get_current().domain)
    return transform(t.render(context), base_url=base_url)


def extend_base_email_template(content, context={}, html=False):
    context.update({
        'email_content': content,
        'protocol': 'http',
        'domain': Site.objects.get_current().domain
    })
    return extend_email_template(
        'emailtemplates/base.%s' % ('html' if html else 'txt'),
        context
    )


def send_email_template(email_template, to_email, context={}, from_email=None, attachments=None):
    context.update({
        'subject': render_string_email_template(email_template.subject, context)
    })
    bcc = []
    if email_template.bcc_email:
        bcc = [email.strip() for email in email_template.bcc_email.split(',')]

    if not from_email:
        from_email = django_settings.DEFAULT_FROM_EMAIL

    if django_settings.DEBUG and hasattr(django_settings, 'DEBUG_EMAIL'):
        to_email = [django_settings.DEBUG_EMAIL]
        bcc = []

    message_plain = render_string_email_template(email_template.get_plain(), context)
    message_html = render_string_email_template(email_template.get_html(), context)

    email = EmailMultiAlternatives(
        render_string_email_template(email_template.subject, context),
        extend_base_email_template(message_plain, context),
        from_email,
        to_email,
        bcc
    )
    email.attach_alternative(
        extend_base_email_template(message_html, context, True),
        'text/html'
    )
    if attachments:
        for attachment in attachments:
            email.attach(attachment['name'], attachment['data'], attachment['type'])
    email.send()
