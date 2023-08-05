from django import forms

from django_support_lite.enums import Priority
from django_support_lite.forms.fields.multiple_file_field import MultipleFileField
from django_support_lite.forms.inputs.multiple_file_input import MultipleFileInput
from django_support_lite.forms.validators.file_content_validator import FileContentValidator


# TODO: use ModelForm
class TicketCreateForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput({
            'class': 'form-control',
        }),
        label='Title',
        help_text='Ticket subject.',
        max_length=300
    )

    text = forms.CharField(
        widget=forms.Textarea({
            'class': 'form-control',
            'rows': 5,
        }),
        label='Text',
        help_text='Ticket message.',
        max_length=100000
    )

    priority = forms.ChoiceField(
        widget=forms.Select({
            'class': 'form-control',
        }),
        label='Priority',
        initial=Priority.NORMAL,
        choices=(
            (priority, Priority.label(priority))
            for priority in (
                Priority.LOW,
                Priority.NORMAL,
                Priority.HIGH,
            )
        )
    )

    images = MultipleFileField(
        widget=MultipleFileInput(),
        validators=[
            FileContentValidator(content_restrictions=[
                {
                    'extensions': [
                        'jpg',
                        'jpeg',
                        'gif',
                        'png',
                    ],
                    'content_types': [
                        'image/jpeg',
                        'image/jpeg',
                        'image/pjpeg',
                        'image/png',
                        'image/gif',
                    ],
                },
            ]),
        ],
        label='Images',
        help_text='Up to 5 images. Format jpg, png, gif.',
        max_count=5,
        required=False
    )
