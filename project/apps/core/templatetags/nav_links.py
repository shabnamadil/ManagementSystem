from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active_link(context, view_name):
    request = context['request']
    if request.resolver_match and request.resolver_match.url_name == view_name:
        return 'active-dot'
    return ''