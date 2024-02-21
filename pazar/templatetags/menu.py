from django import template
from pazar.models import Category

register = template.Library()

@register.inclusion_tag('main/menu.html')

def menu():
    kategoriler = Category.objects.all()
    return {'kategoriler': kategoriler}