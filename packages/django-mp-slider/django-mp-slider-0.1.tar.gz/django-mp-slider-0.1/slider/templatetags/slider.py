
from django import template

from slider.models import SliderImage


register = template.Library()


@register.inclusion_tag('slider.html')
def render_slider():
    return {'slider_photos': SliderImage.objects.all()}
