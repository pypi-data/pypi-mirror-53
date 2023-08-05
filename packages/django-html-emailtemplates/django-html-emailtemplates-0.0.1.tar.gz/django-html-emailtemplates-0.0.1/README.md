# Django HTML Email Templates

A Django app for allowing users to create html emails using Django template variables
passed in to the context.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install django-html-email-templates.

    pip install django-html-email-templates


## Usage

    # models.py
    class Settings(models.Model):
        contact_form_reply = models.ForeignKey(
            'emailtemplates.EmailTemplate'
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


## Features to add
- [ ] Add custom ForeignKey field to display the context that can be used
- [ ] Add plugins for images/documents
- [ ] Add better html field
- [ ] Add support for Wagtail StreamField
