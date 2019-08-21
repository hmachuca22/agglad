# -*- coding: utf-8 -*-
from django.test import TestCase

from training.core.factories import DiplomatFactory, WorkshopFactory, ModuleFactory, TagFactory, TrainingUnitTagFactory
from training.core.models import TrainingUnit


class TrainingUnitTests(TestCase):
    def setUp(self):
        self.tag_1 = TagFactory()
        self.tag_2 = TagFactory()
        self.tag_3 = TagFactory()
        self.tag_4 = TagFactory()
        self.tag_5 = TagFactory()
        self.tag_6 = TagFactory()

        self.diplomat = DiplomatFactory(duration=120, difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE)
        TrainingUnitTagFactory(training_unit=self.diplomat, tag=self.tag_1)

        self.workshop_1 = WorkshopFactory(
            parent=self.diplomat,
            duration=self.diplomat.duration / 2,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.workshop_1, tag=self.tag_2)

        self.module_1_1 = ModuleFactory(
            parent=self.workshop_1,
            duration=self.workshop_1.duration / 2,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.module_1_1, tag=self.tag_3)
        TrainingUnitTagFactory(training_unit=self.module_1_1, tag=self.tag_4)

        self.module_1_2 = ModuleFactory(
            parent=self.workshop_1,
            duration=self.workshop_1.duration / 2,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.module_1_2, tag=self.tag_5)

        self.workshop_2 = WorkshopFactory(
            parent=self.diplomat,
            duration=self.diplomat.duration / 2,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.workshop_2, tag=self.tag_2)

        self.module_2_1 = ModuleFactory(
            parent=self.workshop_2,
            duration=self.workshop_2.duration / 3,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.module_2_1, tag=self.tag_6)

        self.module_2_2 = ModuleFactory(
            parent=self.workshop_2,
            duration=self.workshop_2.duration / 3,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.module_2_2, tag=self.tag_6)

        self.module_2_3 = ModuleFactory(
            parent=self.workshop_2,
            duration=self.workshop_2.duration / 3,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.module_2_3, tag=self.tag_6)

    def test_to_representation(self):
        """ Test para validar la representación de un training plan completo """

        expected_representation = dict(
            id=self.diplomat.id,
            slug=self.diplomat.slug,
            name=self.diplomat.name,
            description=self.diplomat.description,
            content=self.diplomat.content,
            type=TrainingUnit.Type.DIPLOMAT,
            status=self.diplomat.status,
            status_label=self.diplomat.get_status_display(),
            duration=120,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE,
            difficulty_level_label=self.diplomat.get_difficulty_level_display(),
            tags=[
                dict(
                    slug=self.tag_1.slug,
                    display_name=self.tag_1.display_name
                )
            ],
            tags_slugs=[self.tag_1.slug],
            sub_units=[
                dict(
                    id=self.workshop_1.id,
                    slug=self.workshop_1.slug,
                    name=self.workshop_1.name,
                    description=self.workshop_1.description,
                    content=self.workshop_1.content,
                    type=TrainingUnit.Type.WORKSHOP,
                    status=self.workshop_1.status,
                    status_label=self.workshop_1.get_status_display(),
                    duration=60,
                    difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE,
                    difficulty_level_label=self.workshop_1.get_difficulty_level_display(),
                    tags=[
                        dict(
                            slug=self.tag_2.slug,
                            display_name=self.tag_2.display_name
                        )
                    ],
                    tags_slugs=[self.tag_2.slug],
                    sub_units=[
                        dict(
                            id=self.module_1_1.id,
                            slug=self.module_1_1.slug,
                            name=self.module_1_1.name,
                            description=self.module_1_1.description,
                            content=self.module_1_1.content,
                            type=TrainingUnit.Type.MODULE,
                            status=self.module_1_1.status,
                            status_label=self.module_1_1.get_status_display(),
                            duration=30,
                            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE,
                            difficulty_level_label=self.module_1_1.get_difficulty_level_display(),
                            tags=[
                                dict(
                                    slug=self.tag_3.slug,
                                    display_name=self.tag_3.display_name
                                ),
                                dict(
                                    slug=self.tag_4.slug,
                                    display_name=self.tag_4.display_name
                                )
                            ],
                            tags_slugs=[self.tag_3.slug, self.tag_4.slug],
                            sub_units=[]
                        ),
                        dict(
                            id=self.module_1_2.id,
                            slug=self.module_1_2.slug,
                            name=self.module_1_2.name,
                            description=self.module_1_2.description,
                            content=self.module_1_2.content,
                            type=TrainingUnit.Type.MODULE,
                            status=self.module_1_2.status,
                            status_label=self.module_1_2.get_status_display(),
                            duration=30,
                            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE,
                            difficulty_level_label=self.module_1_2.get_difficulty_level_display(),
                            tags=[
                                dict(
                                    slug=self.tag_5.slug,
                                    display_name=self.tag_5.display_name
                                )
                            ],
                            tags_slugs=[self.tag_5.slug],
                            sub_units=[]
                        )
                    ]
                ),
                dict(
                    id=self.workshop_2.id,
                    slug=self.workshop_2.slug,
                    name=self.workshop_2.name,
                    description=self.workshop_2.description,
                    content=self.workshop_2.content,
                    type=TrainingUnit.Type.WORKSHOP,
                    status=self.workshop_2.status,
                    status_label=self.workshop_2.get_status_display(),
                    duration=60,
                    difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE,
                    difficulty_level_label=self.workshop_2.get_difficulty_level_display(),
                    tags=[
                        dict(
                            slug=self.tag_2.slug,
                            display_name=self.tag_2.display_name
                        )
                    ],
                    tags_slugs=[self.tag_2.slug],
                    sub_units=[
                        dict(
                            id=self.module_2_1.id,
                            slug=self.module_2_1.slug,
                            name=self.module_2_1.name,
                            description=self.module_2_1.description,
                            content=self.module_2_1.content,
                            type=TrainingUnit.Type.MODULE,
                            status=self.module_2_1.status,
                            status_label=self.module_2_1.get_status_display(),
                            duration=20,
                            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE,
                            difficulty_level_label=self.module_2_1.get_difficulty_level_display(),
                            tags=[
                                dict(
                                    slug=self.tag_6.slug,
                                    display_name=self.tag_6.display_name
                                )
                            ],
                            tags_slugs=[self.tag_6.slug],
                            sub_units=[]
                        ),
                        dict(
                            id=self.module_2_2.id,
                            slug=self.module_2_2.slug,
                            name=self.module_2_2.name,
                            description=self.module_2_2.description,
                            content=self.module_2_2.content,
                            type=TrainingUnit.Type.MODULE,
                            status=self.module_2_2.status,
                            status_label=self.module_2_2.get_status_display(),
                            duration=20,
                            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE,
                            difficulty_level_label=self.module_2_2.get_difficulty_level_display(),
                            tags=[
                                dict(
                                    slug=self.tag_6.slug,
                                    display_name=self.tag_6.display_name
                                )
                            ],
                            tags_slugs=[self.tag_6.slug],
                            sub_units=[]
                        ),
                        dict(
                            id=self.module_2_3.id,
                            slug=self.module_2_3.slug,
                            name=self.module_2_3.name,
                            description=self.module_2_3.description,
                            content=self.module_2_3.content,
                            type=TrainingUnit.Type.MODULE,
                            status=self.module_2_3.status,
                            status_label=self.module_2_3.get_status_display(),
                            duration=20,
                            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE,
                            difficulty_level_label=self.module_2_3.get_difficulty_level_display(),
                            tags=[
                                dict(
                                    slug=self.tag_6.slug,
                                    display_name=self.tag_6.display_name
                                )
                            ],
                            tags_slugs=[self.tag_6.slug],
                            sub_units=[]
                        )
                    ]
                )
            ]
        )

        self.assertDictEqual(self.diplomat.to_representation(), expected_representation)
