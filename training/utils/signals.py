# -*- coding: utf-8 -*-
from django.conf import settings
from hashids import Hashids
from slugify import slugify


def set_unique_slug(sender, instance, **kwargs):
    """
    Crea y asigna un `slug` único a una instancia recien creada.
    Para asegurar que el slug sea único, se crea un slug del campo `name` de la instancia que está siendo guardada,
    y se le concatena un hash de seis caracteres creado a partir del `id` de la instancia.
    """
    if not instance.slug:
        base_field = kwargs.get('base_field', 'name')
        slug_field = kwargs.get('slug_field', 'slug')

        hashids = Hashids(min_length=6, salt=settings.HASHIDS_SALT)

        hashed_id = hashids.encode(instance.pk)
        slug = slugify(
            text=getattr(instance, base_field),
            max_length=(sender._meta.get_field(slug_field).max_length - len(hashed_id) - 1)
        )

        setattr(instance, slug_field, f'{slug}-{hashed_id}')

        # Hack para instancias que heredan de MPTTModel.
        # Este hack es necesario eunicamente cuando se guardan datos desde el admin site
        # from mptt.models import MPTTModel
        # if isinstance(instance, MPTTModel) and instance.parent:
        #     instance.move_to(instance.parent)

        instance.save(update_fields=[slug_field])


def set_slug(sender, instance, **kwargs):
    """
    Crea y asigna un `slug` a partir del campo `name` de la instancia que está siendo guardada.
    """
    if not instance.slug:
        base_field = kwargs.get('base_field', 'name')
        slug_field = kwargs.get('slug_field', 'slug')

        slug = slugify(text=getattr(instance, base_field), max_length=sender._meta.get_field(slug_field).max_length)

        setattr(instance, slug_field, slug)

        # Hack para instancias que heredan de MPTTModel.
        # Este hack es necesario eunicamente cuando se guardan datos desde el admin site
        # from mptt.models import MPTTModel
        # if isinstance(instance, MPTTModel) and instance.parent:
        #     instance.move_to(instance.parent)

        instance.save(update_fields=[slug_field])
