from django.db import models
from django import forms
from django.forms.fields import Field

from .settings import get_email_template_model


class EmailTemplateWidget(forms.Select):
    template_name = 'emailtemplates/forms/widgets/select.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['email_context'] = self.email_context
        return context


class EmailTemplateFormField(forms.ModelChoiceField):
    widget = EmailTemplateWidget
    def __init__(self, email_context=None, **kwargs):
        super().__init__(**kwargs)
        self.email_context = email_context
        self.widget.email_context = email_context


class EmailTemplateField(models.ForeignKey):
    def __init__(self, on_delete, email_context=None, **kwargs):
        model = get_email_template_model()
        kwargs['to'] = "{0}.{1}".format(model._meta.app_label, model._meta.model_name)
        kwargs['on_delete'] = on_delete
        super().__init__(**kwargs)
        self.email_context = email_context

    def formfield(self, *, using=None, **kwargs):
        if isinstance(self.remote_field.model, str):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.remote_field.model))
        return super().formfield(**{
            'form_class': EmailTemplateFormField,
            'queryset': self.remote_field.model._default_manager.using(using),
            'to_field_name': self.remote_field.field_name,
            'email_context': self.email_context,
            **kwargs,
        })
