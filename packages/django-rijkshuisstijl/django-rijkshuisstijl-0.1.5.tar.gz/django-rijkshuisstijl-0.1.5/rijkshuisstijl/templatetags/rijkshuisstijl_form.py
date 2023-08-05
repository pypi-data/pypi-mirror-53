from django import template

from .rijkshuisstijl import parse_kwarg

register = template.Library()


@register.inclusion_tag('rijkshuisstijl/components/form/form.html', takes_context=True)
def form(context, form=None, label='', **kwargs):
    kwargs['form'] = form or parse_kwarg(kwargs, 'form', context.get('form'))
    kwargs['label'] = label
    kwargs['request'] = context['request']
    return kwargs


@register.inclusion_tag('rijkshuisstijl/components/form/form-control.html')
def form_control(**kwargs):
    return kwargs



@register.inclusion_tag('rijkshuisstijl/components/form/input.html')
def form_input(**kwargs):
    return kwargs
