from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter
def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
