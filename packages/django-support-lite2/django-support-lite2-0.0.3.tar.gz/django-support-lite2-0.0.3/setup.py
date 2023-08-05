from setuptools import setup

setup(
    name='django-support-lite2',
    version='0.0.3',
    description='Django Support Lite 2',
    url='https://nii-ikt.ru/',
    author='nii-ikt',
    author_email='it-director@nii-ikt.ru',
    license='MIT',
    packages=[
        'django_support_lite',
        'django_support_lite.forms.fields',
        'django_support_lite.forms.inputs',
        'django_support_lite.forms.validators',
        'django_support_lite.helpers',
        'django_support_lite.migrations',
        'django_support_lite.models',
        'django_support_lite.templatetags',
        'django_support_lite.views',
        'django_support_lite.views.forms',
    ],
    include_package_data=True,
    zip_safe=False
)
