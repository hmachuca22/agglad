# -*- coding: utf-8 -*-


def copy_tag_to_ancestor(sender, instance, created, **kwargs):

    if created and instance.training_unit.parent is not None:
        sender.objects.get_or_create(
            training_unit=instance.training_unit.parent, tag=instance.tag, defaults={'hidden': True}
        )
