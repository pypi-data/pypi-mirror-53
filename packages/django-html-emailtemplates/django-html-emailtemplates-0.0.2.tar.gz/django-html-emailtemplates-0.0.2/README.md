# Django HTML Email Templates

A Django app for allowing users to create html emails using Django template variables
passed in to the context.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install django-html-emailtemplates.

    pip install django-html-emailtemplates

Add the package to your INSTALLED_APPS

    INSTALLED_APPS = [
        ...
        'emailtemplates',
        ...
    ]


## Usage

    # models.py
    from emailtemplates.fields import EmailTemplateField
    class Settings(models.Model):
        contact_form_reply = EmailTemplateField(
            models.SET_NULL,
            null=True,
            email_context="""
            You can use the following variables in the template:
            {{ name }}
            {{ subject_matter }}
            {% for item in items %}
                Possible values are:
                {{ item.title }}
                {{ item.cost }}
                {{ item.description }}
            {% endfor %}
            """
        )

    # views.py
    from emailtemplates.utils import send_email_template
    from emailtemplates.models import EmailTemplate
    from .models import Settings

    # view definition
    def form_valid(self, form):
        enquiry = form.save()
        # send reply email to website user
        send_email_template(
            Settings.objects.first().contact_form_reply,
            [enquiry.email],
            {
                'name': enquiry.name,
                'subject_matter': enquiry.subject,
                'items': [
                    {
                        'title': 'Product',
                        'cost': '&pound;20.00',
                        'description': 'Product description...'
                    }
                ]
            }
        )
        # send notification to website owner
        send_email_template(
            EmailTemplate(
                subject='Enquiry from example.com',
                content='''<div>
                    <p>There was an enquiry on your website, the details are below:</p>
                    <table>
                        <tbody>
                            <tr>
                                <td>Name:</td>
                                <td>{{ enquiry.name }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>'''
            ),
            ['contact@example.com'],
            {
                'enquiry': enquiry
            }
        )


![alt text](https://github.com/RG1BB5/django-html-emailtemplates/blob/master/example-emailtemplate-field.png "Example EmailTemplateField")


## Features to add
- [ ] Add custom ForeignKey field to display the context that can be used
- [ ] Add base email header/footer
- [ ] Add plugins for images/documents
- [ ] Add better html field
- [ ] Add support for Wagtail StreamField
