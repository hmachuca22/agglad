# -*- coding: utf-8 -*-
import json

from django.test import TestCase

from training.core.factories import TagFactory, WorkshopFactory, ModuleFactory, TrainingUnitTagFactory
from training.core.models import TrainingUnit
from training.core.utils import validate_training_plan_schema, training_plan_from_schema


class ValidateTrainingPlanSchemaTests(TestCase):
    def setUp(self):
        self.valid_training_plan_schema = {
            'name': 'Diplomado de pedagogia',
            'description': 'Diplomado de pedagogia',
            'content': 'Contenido de todo el diplomado...',
            'type': TrainingUnit.Type.DIPLOMAT,
            'duration': 120,
            'difficulty_level': TrainingUnit.DifficultyLevel.BASIC,
            'tags': ['pedagogia', 'historia'],
            'sub_units': [
                {
                    'name': 'Módulo 1',
                    'description': 'Módulo de ética profesional 1',
                    'content': 'En este módulo se estudía el manual de ética que debe regir el comportamiento docente',
                    'type': TrainingUnit.Type.MODULE,
                    'duration': 60,
                    'difficulty_level': TrainingUnit.DifficultyLevel.BASIC
                }, {
                    'name': 'Módulo 2',
                    'description': 'Módulo de ética profesional 2',
                    'content': 'En este módulo se estudía el manual de ética que debe regir el comportamiento docente',
                    'type': TrainingUnit.Type.MODULE,
                    'duration': 60,
                    'difficulty_level': TrainingUnit.DifficultyLevel.BASIC
                }
            ]
        }

    def test_validate_sub_units_duration(self):
        """
        Test para validar que la duración de una unidad sea igual a la suma de la duración de todas las sub unidades
        """
        invalid_training_plan_schema = self.valid_training_plan_schema.copy()
        invalid_training_plan_schema['sub_units'][0]['duration'] = 0

        expected_validated_plan_schema = invalid_training_plan_schema.copy()
        error_message = (
            'La suma de horas de las sub unidades de una unidad, debe ser igual a la duración de la unidad (60 <> 120).'
        )
        expected_validated_plan_schema['sub_units'][0]['duration_errors'] = [error_message]
        expected_validated_plan_schema['sub_units'][1]['duration_errors'] = [error_message]

        valid, validated_plan_schema = validate_training_plan_schema(json.dumps(invalid_training_plan_schema))

        self.assertFalse(valid)
        self.assertDictEqual(validated_plan_schema, expected_validated_plan_schema)

    def test_validate_required_fields(self):
        """ Test para validar que """
        invalid_training_plan_schema = self.valid_training_plan_schema.copy()
        invalid_training_plan_schema.pop('name')

        expected_validated_plan_schema = invalid_training_plan_schema.copy()
        expected_validated_plan_schema['name_errors'] = ['Este campo es requerido.']

        valid, validated_plan_schema = validate_training_plan_schema(json.dumps(invalid_training_plan_schema))

        self.assertFalse(valid)
        self.assertDictEqual(validated_plan_schema, expected_validated_plan_schema)

    def test_successful_validation(self):
        """ Test """
        training_plan_schema = self.valid_training_plan_schema.copy()

        valid, validated_plan_schema = validate_training_plan_schema(json.dumps(training_plan_schema))

        self.assertTrue(valid)


class TrainingPlanFromSchemaTests(TestCase):
    def setUp(self):
        self.tag_1 = TagFactory()
        self.tag_2 = TagFactory()
        self.tag_3 = TagFactory()

        self.valid_training_plan_schema = {
            'name': 'Diplomado de pedagogia',
            'description': 'Diplomado de pedagogia',
            'content': 'Contenido de todo el diplomado...',
            'type': TrainingUnit.Type.DIPLOMAT,
            'duration': 120,
            'difficulty_level': TrainingUnit.DifficultyLevel.BASIC,
            'tags_slugs': [self.tag_1.slug],
            'sub_units': [
                {
                    'name': 'Módulo 1',
                    'description': 'Módulo de ética profesional 1',
                    'content': 'En este módulo se estudía el manual de ética que debe regir el comportamiento docente',
                    'type': TrainingUnit.Type.MODULE,
                    'duration': 60,
                    'difficulty_level': TrainingUnit.DifficultyLevel.BASIC,
                    'tags': [self.tag_2.slug, self.tag_3.slug]
                }, {
                    'name': 'Módulo 2',
                    'description': 'Módulo de ética profesional 2',
                    'content': 'En este módulo se estudía el manual de ética que debe regir el comportamiento docente',
                    'type': TrainingUnit.Type.MODULE,
                    'duration': 60,
                    'difficulty_level': TrainingUnit.DifficultyLevel.BASIC,
                    'tags': [self.tag_1.slug, self.tag_3.slug]
                }
            ]
        }

        self.workshop = WorkshopFactory(duration=120, difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE)
        TrainingUnitTagFactory(training_unit=self.workshop, tag=self.tag_1)

        self.module_1 = ModuleFactory(
            parent=self.workshop,
            duration=self.workshop.duration / 2,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.module_1, tag=self.tag_2)
        TrainingUnitTagFactory(training_unit=self.module_1, tag=self.tag_3)

        self.module_2 = ModuleFactory(
            parent=self.workshop,
            duration=self.workshop.duration / 2,
            difficulty_level=TrainingUnit.DifficultyLevel.INTERMEDIATE
        )
        TrainingUnitTagFactory(training_unit=self.module_2, tag=self.tag_3)

        self.workshop_schema = self.workshop.to_representation()

    def test_create_schema(self):
        """ Test para validar que se cree un training plan completo a partir del esquema proporcionado """
        training_plan_schema = self.valid_training_plan_schema.copy()
        training_plan = training_plan_from_schema(training_plan_schema, status=TrainingUnit.Status.IN_REVIEW)

        # Se valida que se haya creado el nodo raíz correctamente
        self.assertEqual(
            training_plan.id,
            TrainingUnit.objects.get(
                name=self.valid_training_plan_schema['name'],
                description=self.valid_training_plan_schema['description'],
                content=self.valid_training_plan_schema['content'],
                type=self.valid_training_plan_schema['type'],
                duration=self.valid_training_plan_schema['duration'],
                difficulty_level=self.valid_training_plan_schema['difficulty_level'],
                status=TrainingUnit.Status.IN_REVIEW,
                parent=None
            ).id
        )

        # Se valida que se hayan creado cada una de los nodos del training plan con sus respectivos tags
        self.assertTrue(
            TrainingUnit.objects.filter(
                name=self.valid_training_plan_schema['sub_units'][0]['name'],
                description=self.valid_training_plan_schema['sub_units'][0]['description'],
                content=self.valid_training_plan_schema['sub_units'][0]['content'],
                type=self.valid_training_plan_schema['sub_units'][0]['type'],
                duration=self.valid_training_plan_schema['sub_units'][0]['duration'],
                difficulty_level=self.valid_training_plan_schema['sub_units'][0]['difficulty_level'],
                status=TrainingUnit.Status.IN_REVIEW,
                parent=training_plan
            ).exists()
        )

        self.assertTrue(
            TrainingUnit.objects.filter(
                name=self.valid_training_plan_schema['sub_units'][1]['name'],
                description=self.valid_training_plan_schema['sub_units'][1]['description'],
                content=self.valid_training_plan_schema['sub_units'][1]['content'],
                type=self.valid_training_plan_schema['sub_units'][1]['type'],
                duration=self.valid_training_plan_schema['sub_units'][1]['duration'],
                difficulty_level=self.valid_training_plan_schema['sub_units'][1]['difficulty_level'],
                status=TrainingUnit.Status.IN_REVIEW,
                parent=training_plan
            ).exists()
        )

        # Se valida que se hayan creado únicamente los nodo especificados en el esquema
        self.assertEqual(training_plan.get_descendant_count(), 2)

    def test_update_schema(self):
        """ Test para validar que se actualice un training plan existente """
        updated_workshop_schema = self.workshop_schema.copy()
        new_name = 'New workshop name'
        updated_workshop_schema['name'] = new_name
        updated_workshop_schema['sub_units'][0]['difficulty_level'] = TrainingUnit.DifficultyLevel.ADVANCED

        # Llamado al método para actualizar el training plan
        training_plan_from_schema(updated_workshop_schema)

        # Se validan los cambios realizados
        self.assertEqual(TrainingUnit.objects.get(pk=self.workshop.pk).name, new_name)
        self.assertEqual(
            TrainingUnit.objects.get(pk=self.module_1.pk).difficulty_level, TrainingUnit.DifficultyLevel.ADVANCED
        )
