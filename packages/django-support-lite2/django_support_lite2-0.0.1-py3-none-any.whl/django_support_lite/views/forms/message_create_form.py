from django import forms

from django_support_lite.forms.fields.multiple_file_field import MultipleFileField
from django_support_lite.forms.inputs.multiple_file_input import MultipleFileInput
from django_support_lite.forms.validators.file_content_validator import FileContentValidator


# TODO: use ModelForm
class MessageCreateForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea({
            "class": "form-control",
            "rows": 5,
        }),
        label="Text",
        help_text="Ticket message.",
        max_length=100000
    )

    images = MultipleFileField(
        widget=MultipleFileInput(),
        validators=[
            FileContentValidator(content_restrictions=[
                {
                    "extensions": [
                        "jpg",
                        "jpeg",
                        "gif",
                        "png",
                    ],
                    "content_types": [
                        "image/jpeg",
                        "image/jpeg",
                        "image/pjpeg",
                        "image/png",
                        "image/gif",
                    ],
                },
            ]),
        ],
        label="Images",
        help_text="Up to 5 images. Format jpg, png, gif.",
        max_count=5,
        required=False
    )
