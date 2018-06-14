from django import template
from django.utils.html import strip_spaces_between_tags, strip_tags
from django.utils.text import Truncator

register = template.Library()

@register.filter(name='excerpt')
def excerpt_with_ptag_spacing(value):

    # remove spaces between tags
    #value = strip_spaces_between_tags(value)

    # add space before each P end tag (</p>)
    value = value.replace("</p>"," </p>")

    # strip HTML tags
    value = strip_tags(value)

    # other usage: return Truncator(value).words(length, html=True, truncate=' see more')
    return value
