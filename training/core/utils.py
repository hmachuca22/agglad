# -*- coding: utf-8 -*-
import json

from .forms import TrainingUnitForm
from .models import Tag, TrainingUnit, TrainingUnitTag


def validate_training_plan_schema(schema):
    """
    Valida el esquema para crear o actualizar un training-plan completo. En caso que el esquema no sea válido,
    se retorna el esquema con los errores encontrados.

    Args:
        schema (str): Esquema a validar

    Returns:
        valid (bool): `True` en caso de ser un esquema completo válido, `False` en caso contrario
        validated_plan_schema (dict): El esquema con los posibles mensajes de error
    """
    try:
        schema = json.loads(schema)
        valid_training_plan, validated_training_plan = validate_training_unit_schema(schema.copy())

    except Exception:
        return False, schema

    else:
        return valid_training_plan, validated_training_plan


def validate_training_unit_schema(unit_schema, parent_schema=None):
    """
    Valida el esquema de un training-unit. Esto conlleva validar el esquema de la unidad y los esquemas de cada una
    de las sub unidades que pertenecen a la unidad.

    Returns:
        valid_schema (bool): `True` en caso de ser un esquema válido, `False` en caso contrario
        validated_unit_schema (dict):
    """
    valid_unit = True
    valid_sub_units = True

    form_kwargs = dict(data=unit_schema)
    if unit_schema.get('id', None):
        form_kwargs['instance'] = TrainingUnit.objects.get(id=unit_schema['id'])
    unit = TrainingUnitForm(**form_kwargs)

    if unit.is_valid():
        sub_units = unit_schema.get('sub_units', [])
        if sub_units:
            valid_sub_units, unit_schema['sub_units'] = validate_sub_units_schemas(sub_units, parent_schema=unit_schema)

    else:
        valid_unit = False
        for field, error in unit.errors.items():
            unit_schema[f'{field}_errors'] = error

    return bool(valid_unit and valid_sub_units), unit_schema


def validate_sub_units_schemas(sub_units, parent_schema):
    """
    Valida que las sub unidades de una unidad estén configuradas correctamente. Esto incluye que:
    - La suma de las duraciones de todas las sub unidades sea igual a la duración de la unidad a la que pertenecen
    - Que el tipo de cada sub unidad sea válido dependiendo del tipo de la unidad

    Args:
        sub_units (list): Listado de sub unidades a validar
        parent_schema (dict): Esquema de la unidad a la cual pertenecen las sub unidades

    Returns:
        valid_sub_units (bool): `True` en caso que todos las sub unidades sean válidas, `False` en caso contrario
        validated_sub_units (list): Listado de sub unidades validadas
    """
    valid_sub_units = True

    sub_units_duration = 0
    for index, sub_unit in enumerate(sub_units):
        valid_sub_units, sub_units[index] = validate_training_unit_schema(
            unit_schema=sub_unit, parent_schema=parent_schema
        )

        if valid_sub_units:
            sub_units_duration += sub_unit['duration']
        else:
            return False, sub_units

    if sub_units_duration != parent_schema['duration']:
        valid_sub_units = False
        for index, sub_unit in enumerate(sub_units):
            sub_units[index]['duration_errors'] = [
                (
                    'La suma de horas de las sub unidades de una unidad, debe ser igual a la duración de la unidad '
                    f'({sub_units_duration} <> {parent_schema["duration"]}).'
                )
            ]

    return valid_sub_units, sub_units


def training_plan_from_schema(schema, status="draft", parent=None):
    """
    Crea la estructura completa de un training plan a partir de su representación.

    Args:
         schema (dict): Esquema a partir del cual se debe crear o actualizar el training plan
         status (string): Estado del tra
         parent (object):

    Returns:
        training (obj): Objeto root del training plan
    """
    # Creación/actualización del nodo raíz del esquema
    unit, _ = TrainingUnit.objects.update_or_create(
        id=schema.get('id', None),
        defaults=dict(
            name=schema['name'],
            description=schema['description'],
            content=schema['content'],
            order=schema.get('order', 1),
            type=schema['type'],
            parent=parent,
            duration=schema['duration'],
            difficulty_level=schema['difficulty_level'],
            status=status
        )
    )

    # Primero se eliminan todos los tags asociados que no se encuentren en la lista de tags
    # Luego se cran o actualizan
    tags_slugs = schema.get('tags_slugs', [])
    TrainingUnitTag.objects.filter(training_unit=unit).exclude(tag__slug__in=tags_slugs).delete()
    for slug in tags_slugs:
        TrainingUnitTag.objects.update_or_create(
            training_unit=unit,
            tag=Tag.objects.get(slug=slug),
            defaults=dict(
                hidden=False
            )
        )

    # Creación de los sub nodos del esquema
    for index, sub_unit in enumerate(schema.get('sub_units', []), start=1):
        sub_unit['order'] = index
        training_plan_from_schema(schema=sub_unit, status=status, parent=unit)

    return unit
