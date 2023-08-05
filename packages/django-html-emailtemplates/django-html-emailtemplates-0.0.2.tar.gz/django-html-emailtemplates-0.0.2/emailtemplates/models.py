from django.db import models
from django.utils.translation import ugettext_lazy as _
from bs4 import BeautifulSoup
import re
try:
    from djangocms_text_ckeditor.fields import HTMLField
except ImportError:
    try:
        from tinymce.models import HTMLField
    except ImportError:
        try:
            from ckeditor.fields import RichTextField as HTMLField
        except ImportError:
            raise ImportError('You need to have one of the following packages installed: (djangocms_text_ckeditor, tinymce or ckeditor)')

from . import settings

class BaseEmailTemplate(models.Model):
    class Meta:
        verbose_name = _('E-Mail Template')
        verbose_name_plural = _('E-Mail Templates')
        abstract = True

    subject = models.CharField(
        _('Subject'),
        max_length=255,
    )

    cc_email = models.CharField(
        _('CC E-Mail'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('You can provide an E-Mail address (or multiple using a comma seperated list) to cc all E-Mails sent using this template.')
    )

    bcc_email = models.CharField(
        _('BCC E-Mail'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('You can provide an E-Mail address (or multiple using a comma seperated list) to bcc all E-Mails sent using this template.')
    )

    content = HTMLField(
        help_text=_('This is the content that will be sent when this template is used.')
    )

    def get_html(self):
        if settings.ALLOWS_LOOPS:
            return self.get_loops(self.content)
        return self.content

    def get_plain(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        if settings.ALLOWS_LOOPS:
            soup = BeautifulSoup(self.get_loops(self.content), 'html.parser')
        return soup.get_text()

    def get_loops(self, template_string):
        construction_string = template_string
        result = re.search('{%% forloop(.*)endfor %%}', template_string, re.DOTALL)
        if result:
            test = result.group()

            # remove open tag
            tag = re.search('{%%(.*)%%}', test)
            open_tag = tag.group().replace('%%', '%').replace('forloop', 'for').split()
            open_tag = ' '.join(open_tag[0:-2] + ['in'] + open_tag[-2:])
            test = test[0:tag.span()[0]] + test[tag.span()[1]:]

            # remove close tag
            close = re.search('{%%(.*)%%}', test)
            close_tag = close.group().replace('%%', '%').split()
            close_tag = ' '.join(close_tag)
            test = test[0:close.span()[0]] + test[close.span()[1]:]

            soup = BeautifulSoup(test, 'html.parser')
            forloop_elem = soup.findAll(class_="forloop")

            if forloop_elem:
                replace_string = ''
                node = forloop_elem[0]
                node.contents = []
                node.string = '(.*)'

                pp = re.search(str(node), test, re.DOTALL)
                if pp:
                    test = test[:pp.span()[0]] + open_tag + test[pp.span()[0]:]
                    test = test[:pp.span()[1] + len(open_tag)] + close_tag + test[pp.span()[1] + len(open_tag):]

            template_string = template_string[0:result.span()[0]] + test + template_string[result.span()[1]:]
        return template_string

    def __str__(self):
        return self.subject

    def __unicode__(self):
        return unicode(self.subject)


class EmailTemplate(BaseEmailTemplate):
    class Meta:
        verbose_name = _('E-Mail Template')
        verbose_name_plural = _('E-Mail Templates')

    title = models.CharField(
        max_length=255,
        help_text=_('This is just for reference.')
    )

    def __str__(self):
        return self.title


class EmailTemplateSettings(models.Model):
    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')

    test_emails = models.CharField(
        _('Test emails'),
        max_length=255,
        null=True,
        help_text=_('This can be a list of E-Mails seperated by comma(,).')
    )

    def __str__(self):
        return 'Email Template Settings'

    def __unicode__(self):
        return unicode('Email Template Settings')

    @classmethod
    def get(cls):
        return cls.objects.first()
