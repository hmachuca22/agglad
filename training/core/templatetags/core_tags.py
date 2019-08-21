# -*- coding: utf-8 -*-
from django import template
from training.core.models import TrainingUnit, Tag
from training.enrollment.models import Group, Enrollment
from training.users.models import User, UserEmployeeType
from training.spaces.models import TrainingSpace
register = template.Library()


@register.inclusion_tag('core/training_unit_form.html', takes_context=True)
def training_unit_form(
    context, training_unit, is_root=True, depth_level=0, component_prefix='0-', parent_component_prefix=''
):
    """
    Renderiza el formulario para crear y actualizar las unidades de un training plan.
    Este template tag sen encarga también de renderizar training unit ocultos
    """

    # TODO: Buscar una mejor forma de agregar training units ocultos
    sub_units = training_unit.get('sub_units', [])
    if len(component_prefix) <= 6:
        sub_units.extend([{'hidden': True}] * 3)

    return {
        'training_unit': training_unit,
        'hidden': training_unit.get('hidden', False),
        'sub_units': sub_units,
        'types': context['types'],
        'difficulty_levels': context['difficulty_levels'],
        'tags': context['tags'],
        'is_root': is_root,
        'depth_level': depth_level,
        'component_prefix': component_prefix,
        'parent_component_prefix': parent_component_prefix
    }


@register.filter
def concatenate(arg1, arg2):
    return str(arg1) + str(arg2)


@register.filter
def unit_type_tag(arg):
    choices = dict(TrainingUnit.Type.CHOICES)
    return choices.get(arg, "")


@register.filter
def unit_level_tag(arg):
    choices = dict(TrainingUnit.DifficultyLevel.CHOICES)
    return choices.get(arg, "")


@register.filter
def group_mod_tag(arg):
    choices = dict(Group.Modality.CHOICES)
    return choices.get(arg, "")


@register.filter
def user_gender_tag(arg):
    choices = dict(User.Gender.CHOICES)
    return choices.get(arg, "")


@register.filter
def unit_tags(arg):
    choices = dict(Tag.objects.all().values_list('slug','display_name'))
    return choices.get(arg, "")


@register.filter
def space_type_tag(arg):
    choices = dict(TrainingSpace.Type.CHOICES)
    return choices.get(arg, "")


@register.filter
def employee_type_tag(arg):
    choices = dict(UserEmployeeType.Type.CHOICES)
    return choices.get(arg, "")


@register.filter
def status_tag(arg):
    choices = dict(Enrollment.Status.CHOICES)
    return choices.get(arg, "")