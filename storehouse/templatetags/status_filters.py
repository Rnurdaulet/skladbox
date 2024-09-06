from django import template

register = template.Library()

STATUS_CHOICES = {
    'accepted': 'Принято',
    'delivered': 'Доставлено',
    'issued': 'Выдано'
}


@register.filter
def translate_status(value):
    """Переводит статус на русский язык."""
    return STATUS_CHOICES.get(value, value)
