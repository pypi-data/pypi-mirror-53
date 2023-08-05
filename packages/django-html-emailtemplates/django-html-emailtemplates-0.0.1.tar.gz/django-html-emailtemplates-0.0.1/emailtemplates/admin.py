from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin, messages
from django.urls import reverse

from collections import OrderedDict

from .utils.email import send_email_template
from .settings import get_email_template_model, get_email_template_settings_model

EmailTemplate = get_email_template_model()
EmailTemplateSettings = get_email_template_settings_model()
IS_POPUP_VAR = '_popup'


if EmailTemplateSettings:
    class EmailTemplateSettingsAdmin(admin.ModelAdmin):
        def has_add_permission(self, request):
            return False if self.model.objects.count() > 0 else super(EmailTemplateSettingsAdmin, self).has_add_permission(request)
    admin.site.register(EmailTemplateSettings, EmailTemplateSettingsAdmin)

class EmailTemplateAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        """
        Return a dictionary mapping the names of all actions for this
        ModelAdmin to a tuple of (callable, name, description) for each action.
        """
        # If self.actions is explicitly set to None that means that we don't
        # want *any* actions enabled on this page.
        if self.actions is None or IS_POPUP_VAR in request.GET:
            return OrderedDict()

        actions = []

        # Gather actions from the admin site first
        for (name, func) in self.admin_site.actions:
            description = getattr(func, 'short_description', name.replace('_', ' '))
            actions.append((func, name, description))

        # Then gather them from the model admin and all parent classes,
        # starting with self and working back up.
        for klass in self.__class__.mro()[::-1]:
            class_actions = getattr(klass, 'actions', [])
            # Avoid trying to iterate over None
            if not class_actions:
                continue

            actions.extend(self.get_action(action) for action in class_actions)

        if EmailTemplateSettings:
            et_settings = EmailTemplateSettings.get()
            if hasattr(et_settings, 'test_emails'):
                actions.extend(self.get_action(action) for action in ['test_email'])
        else:
            actions.extend(self.get_action(action) for action in ['test_email'])

        # get_action might have returned None, so filter any of those out.
        actions = filter(None, actions)

        # Convert the actions into an OrderedDict keyed by name.
        actions = OrderedDict(
            (name, (func, name, desc))
            for func, name, desc in actions
        )

        return actions

    def test_email(modeladmin, request, queryset):
        if EmailTemplateSettings:
            et_settings = EmailTemplateSettings.get()
        if hasattr(et_settings, 'test_emails'):
            for emailtemplate in queryset:
                send_email_template(
                    emailtemplate,
                    [et_settings.test_emails],
                    {
                        'user': request.user,
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'subject_matter': 'Order 123',
                        'subject': 'Thank you for your order.',
                        'items': [
                            {
                                'title': 'Developer book',
                                'cost': '&pound;20.00',
                                'description': 'The developer book for all developers.'
                            },
                            {
                                'title': 'Developer book',
                                'cost': '&pound;20.00',
                                'description': 'The developer book for all developers.'
                            },
                            {
                                'title': 'Developer book',
                                'cost': '&pound;20.00',
                                'description': 'The developer book for all developers.'
                            }
                        ]
                    }
                )
        else:
            messages.add_message(request, messages.ERROR, 'There isn\'t a test_emails field set')
    test_email.short_description = 'Send as a test email.'
admin.site.register(EmailTemplate, EmailTemplateAdmin)
