from django import template

register = template.Library()

@register.simple_tag
def status_color(status):
    """Возвращает цветовой класс для статуса."""
    status_colors = {
        'accepted': 'badge-primary',
        'delivered': 'badge-info',
        'issued': 'badge-success'
    }
    return status_colors.get(status, 'badge-secondary')  # 'badge-secondary' для неизвестных статусов
