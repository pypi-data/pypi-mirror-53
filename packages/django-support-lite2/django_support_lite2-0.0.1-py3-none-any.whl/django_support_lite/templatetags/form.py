from django.template import Library

register = Library()


@register.filter
def form_field_class(field):
    return field.field.widget.__class__.__name__

@register.filter
def form_field_group(field, groups):
    if field not in groups:
        return None

    return groups[field]
