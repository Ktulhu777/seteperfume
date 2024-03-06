from django import template
from django.db.models import Count
from men.models import Category

register = template.Library()


@register.inclusion_tag('men/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}
