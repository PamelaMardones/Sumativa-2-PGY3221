from django import template
import locale

register = template.Library()

@register.filter(name='format_amount')
def format_amount(value):
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    value = float(value)
    return locale.currency(value, grouping=True, symbol=False)