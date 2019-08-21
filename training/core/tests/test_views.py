# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from django.urls import reverse

from training.core.factories import TagFactory
from training.core.models import TrainingUnit


class TrainingPlanCRUViewTests(TestCase):
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
            'tags': [self.tag_1.slug],
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

    def test_create_training_plan_and_redirects_to_training_plans_list(self):
        """
        Test para validar que se cree correctamente el training plan y luego se redireccione hacia el listado de
        training plans
        """
        training_plan_schema = self.valid_training_plan_schema.copy()

        response = self.client.post(
            reverse('core:training-plan-add'),
            data={
                'training_plan_schema': json.dumps(training_plan_schema),
                'training_plan_status': TrainingUnit.Status.DRAFT
            }
        )

        # Se valida que se redireccione hacia el listado de training plans
        self.assertRedirects(response, reverse('core:training-plan-list'), fetch_redirect_response=False)

        # Se valida que existan cada uno de los nodos del training plan
        self.assertTrue(
            TrainingUnit.objects.filter(
                name=training_plan_schema['name'],
                description=training_plan_schema['description'],
                content=training_plan_schema['content'],
                type=training_plan_schema['type'],
                duration=training_plan_schema['duration'],
                difficulty_level=training_plan_schema['difficulty_level'],
                status=TrainingUnit.Status.DRAFT,
                parent=None
            ).exists()
        )

        self.assertTrue(
            TrainingUnit.objects.filter(
                name=training_plan_schema['sub_units'][0]['name'],
                description=training_plan_schema['sub_units'][0]['description'],
                content=training_plan_schema['sub_units'][0]['content'],
                type=training_plan_schema['sub_units'][0]['type'],
                duration=training_plan_schema['sub_units'][0]['duration'],
                difficulty_level=training_plan_schema['sub_units'][0]['difficulty_level'],
                status=TrainingUnit.Status.DRAFT,
                parent__isnull=False
            ).exists()
        )

        self.assertTrue(
            TrainingUnit.objects.filter(
                name=training_plan_schema['sub_units'][1]['name'],
                description=training_plan_schema['sub_units'][1]['description'],
                content=training_plan_schema['sub_units'][1]['content'],
                type=training_plan_schema['sub_units'][1]['type'],
                duration=training_plan_schema['sub_units'][1]['duration'],
                difficulty_level=training_plan_schema['sub_units'][1]['difficulty_level'],
                status=TrainingUnit.Status.DRAFT,
                parent__isnull=False
            ).exists()
        )

    def test_create_training_plan_and_redirects_to_update_view(self):
        """
        Test para validar que se cree correctamente el training plan y se redireccione al usuario para que pueda seguir
        editando el training plan
        """
        training_plan_schema = self.valid_training_plan_schema.copy()

        response = self.client.post(
            reverse('core:training-plan-add'),
            data={
                'training_plan_schema': json.dumps(training_plan_schema),
                'training_plan_status': TrainingUnit.Status.DRAFT,
                'continue_editing': True
            }
        )

        training_plan = TrainingUnit.objects.get(
            name=training_plan_schema['name'],
            description=training_plan_schema['description'],
            content=training_plan_schema['content'],
            type=training_plan_schema['type'],
            duration=training_plan_schema['duration'],
            difficulty_level=training_plan_schema['difficulty_level'],
            status=TrainingUnit.Status.DRAFT,
            parent=None
        )

        # Se valida que se redireccione hacia el listado de training plans
        self.assertRedirects(
            response=response,
            expected_url=reverse('core:training-plan-update', kwargs={'slug': training_plan.slug}),
            fetch_redirect_response=False
        )

        self.assertTrue(
            TrainingUnit.objects.filter(
                name=training_plan_schema['sub_units'][0]['name'],
                description=training_plan_schema['sub_units'][0]['description'],
                content=training_plan_schema['sub_units'][0]['content'],
                type=training_plan_schema['sub_units'][0]['type'],
                duration=training_plan_schema['sub_units'][0]['duration'],
                difficulty_level=training_plan_schema['sub_units'][0]['difficulty_level'],
                status=TrainingUnit.Status.DRAFT,
                parent=training_plan
            ).exists()
        )

        self.assertTrue(
            TrainingUnit.objects.filter(
                name=training_plan_schema['sub_units'][1]['name'],
                description=training_plan_schema['sub_units'][1]['description'],
                content=training_plan_schema['sub_units'][1]['content'],
                type=training_plan_schema['sub_units'][1]['type'],
                duration=training_plan_schema['sub_units'][1]['duration'],
                difficulty_level=training_plan_schema['sub_units'][1]['difficulty_level'],
                status=TrainingUnit.Status.DRAFT,
                parent=training_plan
            ).exists()
        )


class TrainingPlanDeleteViewTests(TestCase):
    def setUp(self):
        pass
