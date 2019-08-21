# -*- coding: utf-8 -*-
from urllib.parse import urlencode

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from training.core import factories as core_factories
from training.core import constants as core_constants
from training.core import models as core_models
from training.spaces.factories import AuditoriumFactory, ComputerLabFactory, WebPortalFactory
from training.spaces.models import TrainingSpace
from training.organizations import factories as organizations_factories
from training.organizations import models as organization_models


class AreaListAPIViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hn = core_factories.CountryFactory(name='Honduras', code='hn')

        cls.atlantida = core_factories.StateFactory(
            name=core_constants.State.ATLANTIDA.name, code=core_constants.State.ATLANTIDA.code, parent=cls.hn
        )
        cls.la_ceiba = core_factories.CountyFactory(name='La Ceiba', code='01', parent=cls.atlantida)
        cls.el_porvenir = core_factories.CountyFactory(name='El Porvenir', code='02', parent=cls.atlantida)
        cls.esparta = core_factories.CountyFactory(name='Esparta', code='03', parent=cls.atlantida)

        cls.colon = core_factories.StateFactory(
            name=core_constants.State.COLON.name, code=core_constants.State.COLON.code, parent=cls.hn
        )

        cls.gt = core_factories.CountryFactory(code='gt', name='Guatemala')

    def test_retrieve_all_countries(self):
        """ Test para validar que se retornen todos los países disponibles """
        view_url = reverse('api:countries')
        response = self.client.get(view_url)

        expected_response = [
            self.gt.to_representation(),
            self.hn.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_retrieve_states_for_specific_country(self):
        """ Test para validar que se retornen los departamentos de un país específico """
        view_url = reverse('api:states', kwargs={'country_code': self.hn.code})
        response = self.client.get(view_url)

        expected_response = [
            self.atlantida.to_representation(),
            self.colon.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_empty_list_when_no_state_exist_for_a_given_country(self):
        """ Test para validar que se retorne 200 cuando no existen departamentos registrados para el país solicitado """
        view_url = reverse('api:states', kwargs={'country_code': self.gt.code})
        response = self.client.get(view_url)

        expected_response = []

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_retrieve_counties_for_specific_state(self):
        """ Test para validar que se retornen los municipios de un departamento específico """
        view_url = reverse('api:counties', kwargs={'country_code': self.hn.code, 'state_code': self.atlantida.code})
        response = self.client.get(view_url)

        expected_response = [
            self.la_ceiba.to_representation(),
            self.el_porvenir.to_representation(),
            self.esparta.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_empty_list_when_no_county_exist_for_a_given_state(self):
        """ Test para validar que se retorne 200 cuando no existen departamentos registrados para el país solicitado """
        view_url = reverse('api:counties', kwargs={'country_code': self.hn.code, 'state_code': self.colon.code})
        response = self.client.get(view_url)

        expected_response = []

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)


class TrainingSpaceListAPIViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hn = core_factories.CountryFactory(name='Honduras', code='hn')

        cls.atlantida = core_factories.StateFactory(
            name=core_constants.State.ATLANTIDA.name, code=core_constants.State.ATLANTIDA.code, parent=cls.hn
        )
        cls.la_ceiba = core_factories.CountyFactory(name='La Ceiba', code='01', parent=cls.atlantida)
        cls.el_porvenir = core_factories.CountyFactory(name='El Porvenir', code='02', parent=cls.atlantida)
        cls.esparta = core_factories.CountyFactory(name='Esparta', code='03', parent=cls.atlantida)

        cls.regional_center = organizations_factories.RegionalCenterFactory()
        cls.ngo = organizations_factories.NGOFactory()

        cls.la_ceiba_auditorium = AuditoriumFactory(location=cls.la_ceiba, organization=cls.regional_center)
        cls.el_porvenir_auditorium = AuditoriumFactory(location=cls.el_porvenir, organization=cls.ngo)
        cls.el_porvenir_computer_lab = ComputerLabFactory(location=cls.el_porvenir, organization=cls.regional_center)

        cls.web_portal = WebPortalFactory()

    def test_returns_all_physical_spaces_when_no_filter_is_provided(self):
        """
        Test para validar que se retornen todos los espacios físicos disponibles cuando no se provee ningún filtro
        """
        view_url = reverse('api:physical-spaces')
        response = self.client.get(view_url)

        expected_response = [
            self.la_ceiba_auditorium.to_representation(),
            self.el_porvenir_auditorium.to_representation(),
            self.el_porvenir_computer_lab.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_physical_spaces_filtered_by_type(self):
        """ Test para validar que se retornen los espacios disponibles filtrados por tipo """
        view_url = reverse('api:physical-spaces')
        query_string = urlencode({'type': [TrainingSpace.Type.AUDITORIUM]}, doseq=True)
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.la_ceiba_auditorium.to_representation(),
            self.el_porvenir_auditorium.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_physical_spaces_filtered_by_organization(self):
        """ Test para validar que se retornen los espacios disponibles filtrados por organización """
        view_url = reverse('api:physical-spaces')
        query_string = urlencode({'organization': [self.ngo.id]}, doseq=True)
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.el_porvenir_auditorium.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_physical_spaces_filtered_by_location(self):
        """ Test para validar que se retornen los espacios disponibles filtrados por ubicación """
        view_url = reverse('api:physical-spaces')
        query_string = urlencode({'location': [self.la_ceiba.id]}, doseq=True)
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.la_ceiba_auditorium.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_physical_spaces_filtered_by_location_including_descendant_locations(self):
        """
        Test para validar que se retornen los espacios disponibles filtrados por ubicación y los sitios que componen
        dicha ubicación
        """
        view_url = reverse('api:physical-spaces')
        query_string = urlencode({'location': [self.atlantida.id]}, doseq=True)
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.la_ceiba_auditorium.to_representation(),
            self.el_porvenir_auditorium.to_representation(),
            self.el_porvenir_computer_lab.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_all_virtual_spaces(self):
        """ Test para validar que se retornen todos los espacios virtuales """
        view_url = reverse('api:virtual-spaces')
        response = self.client.get(view_url)

        expected_response = [
            self.web_portal.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)


class OrganizationListAPIViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hn = core_factories.CountryFactory(name='Honduras', code='hn')
        cls.atlantida = core_factories.StateFactory(
            name=core_constants.State.ATLANTIDA.name, code=core_constants.State.ATLANTIDA.code, parent=cls.hn
        )
        cls.la_ceiba = core_factories.CountyFactory(name='La Ceiba', code='01', parent=cls.atlantida)
        cls.el_porvenir = core_factories.CountyFactory(name='El Porvenir', code='02', parent=cls.atlantida)
        cls.esparta = core_factories.CountyFactory(name='Esparta', code='03', parent=cls.atlantida)

        cls.colon = core_factories.StateFactory(
            name=core_constants.State.COLON.name, code=core_constants.State.COLON.code, parent=cls.hn
        )

        cls.departamental_1 = organizations_factories.DepartmentalFactory(code='01')
        organizations_factories.OrganizationAreaFactory(organization=cls.departamental_1, area=cls.atlantida)

        cls.district_1 = organizations_factories.DistrictFactory(code='01')
        organizations_factories.OrganizationAreaFactory(organization=cls.district_1, area=cls.la_ceiba)

        cls.ngo_1 = organizations_factories.NGOFactory(code='ngo1')
        cls.ngo_2 = organizations_factories.NGOFactory(code='ngo2')

        cls.regional_center_1 = organizations_factories.RegionalCenterFactory(code='01')
        organizations_factories.OrganizationAreaFactory(organization=cls.regional_center_1, area=cls.atlantida)

        cls.regional_center_2 = organizations_factories.RegionalCenterFactory(code='02')
        organizations_factories.OrganizationAreaFactory(organization=cls.regional_center_2, area=cls.colon)

        cls.regional_center_3 = organizations_factories.RegionalCenterFactory(code='03')
        cls.regional_center_4 = organizations_factories.RegionalCenterFactory(code='04')

    def test_returns_all_organizations(self):
        """ Test para validar que se obtengan todas las organizaciones """
        view_url = reverse('api:organizations')
        response = self.client.get(view_url)

        expected_response = [
            self.departamental_1.to_representation(),
            self.district_1.to_representation(),
            self.ngo_1.to_representation(),
            self.ngo_2.to_representation(),
            self.regional_center_1.to_representation(),
            self.regional_center_2.to_representation(),
            self.regional_center_3.to_representation(),
            self.regional_center_4.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_organizations_filtered_by_type(self):
        """ Test para validar que se obtenga un listado de organizaciones filtradas por tipo """
        view_url = reverse('api:organizations')
        query_string = urlencode(
            {'type': [organization_models.Organization.Type.REGIONAL_CENTER]}, doseq=True
        )
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.regional_center_1.to_representation(),
            self.regional_center_2.to_representation(),
            self.regional_center_3.to_representation(),
            self.regional_center_4.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_organizations_filtered_by_location(self):
        """ Test para validar que se obtenga un listado de organizaciones filtradas por jurisdicción """
        view_url = reverse('api:organizations')
        query_string = urlencode(
            {'location': [self.atlantida.id, self.colon.id]}, doseq=True
        )
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.departamental_1.to_representation(),
            self.district_1.to_representation(),
            self.regional_center_1.to_representation(),
            self.regional_center_2.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

    def test_returns_organizations_filtered_by_type_and_location(self):
        """ Test para validar que se obtenga un listado de organizaciones filtradas por tipo y jurisdicción """
        view_url = reverse('api:organizations')
        query_string = urlencode(
            {
                'type': [
                    organization_models.Organization.Type.REGIONAL_CENTER,
                    organization_models.Organization.Type.DEPARTMENTAL
                ],
                'location': [self.atlantida.id, self.colon.id]
            },
            doseq=True
        )
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.departamental_1.to_representation(),
            self.regional_center_1.to_representation(),
            self.regional_center_2.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)

class TrainingCallListAPIViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag_1 = core_factories.TagFactory()
        cls.tag_2 = core_factories.TagFactory()
        cls.tag_3 = core_factories.TagFactory()
        cls.tag_4 = core_factories.TagFactory()

        """
        ├── diplomat
        │   ├── workshop 1
        │   │   ├── module 1 [#tag1, #tag2]
        │   │   └── module 2 [#tag1]
        │   └── workshop 2 [#tag1, #tag3]
        └── seminar
            ├── module 1 [#tag4]
            ├── module 2 [#tag1, #tag3, #tag4]
            └── module 3 [#tag2, #tag3]
        """
        cls.diplomat = core_factories.DiplomatFactory()
        cls.diplomat_workshop_1 = core_factories.WorkshopFactory(parent=cls.diplomat)
        cls.diplomat_workshop_1_module_1 = core_factories.ModuleFactory(parent=cls.diplomat_workshop_1)
        cls.diplomat_workshop_1_module_2 = core_factories.ModuleFactory(parent=cls.diplomat_workshop_1)
        cls.diplomat_workshop_2 = core_factories.WorkshopFactory(parent=cls.diplomat)

        core_factories.TrainingUnitTagFactory(training_unit=cls.diplomat_workshop_1_module_1, tag=cls.tag_1)
        core_factories.TrainingUnitTagFactory(training_unit=cls.diplomat_workshop_1_module_1, tag=cls.tag_2)
        core_factories.TrainingUnitTagFactory(training_unit=cls.diplomat_workshop_1_module_2, tag=cls.tag_1)
        core_factories.TrainingUnitTagFactory(training_unit=cls.diplomat_workshop_2, tag=cls.tag_1)
        core_factories.TrainingUnitTagFactory(training_unit=cls.diplomat_workshop_2, tag=cls.tag_3)

        cls.seminar = core_factories.SeminarFactory()
        cls.seminar_module_1 = core_factories.ModuleFactory(parent=cls.seminar)
        cls.seminar_module_2 = core_factories.ModuleFactory(parent=cls.seminar)
        cls.seminar_module_3 = core_factories.ModuleFactory(parent=cls.seminar)

        core_factories.TrainingUnitTagFactory(training_unit=cls.seminar_module_1, tag=cls.tag_4)
        core_factories.TrainingUnitTagFactory(training_unit=cls.seminar_module_2, tag=cls.tag_1)
        core_factories.TrainingUnitTagFactory(training_unit=cls.seminar_module_2, tag=cls.tag_3)
        core_factories.TrainingUnitTagFactory(training_unit=cls.seminar_module_2, tag=cls.tag_4)
        core_factories.TrainingUnitTagFactory(training_unit=cls.seminar_module_3, tag=cls.tag_2)
        core_factories.TrainingUnitTagFactory(training_unit=cls.seminar_module_3, tag=cls.tag_3)

        cls.scheduled_diplomat_training_call = core_factories.ScheduledTrainingCallFactory(
            training_plan=cls.diplomat
        )
        cls.in_progress_diplomat_training_call = core_factories.InProgressTrainingCallFactory(
            training_plan=cls.diplomat
        )
        cls.finished_diplomat_training_call = core_factories.FinishedTrainingCallFactory(
            training_plan=cls.diplomat
        )

        cls.scheduled_seminar_training_call = core_factories.ScheduledTrainingCallFactory(
            training_plan=cls.seminar, start_date=None, end_date=None
        )
        cls.in_progress_seminar_training_call = core_factories.InProgressTrainingCallFactory(
            training_plan=cls.seminar
        )
        cls.finished_seminar_training_call = core_factories.FinishedTrainingCallFactory(
            training_plan=cls.seminar
        )

    def test_retrieve_paginated_training_calls_without_filtering(self):
        """ Test para validar que se retornen las ofertas de formación existentes paginadas """
        view_url = reverse('api:training-calls')
        query_string = urlencode(
            query={
                'page_size': 2
            },
            doseq=True
        )
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.scheduled_seminar_training_call.to_representation(),
            self.scheduled_diplomat_training_call.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data['results'], expected_response)

    def test_retrieve_training_calls_by_status(self):
        """ Test para validar que se retornen ofertas de formación de los estados especificados """
        view_url = reverse('api:training-calls')
        query_string = urlencode(
            query={
                'status': [
                    core_models.TrainingCall.Status.SCHEDULED,
                    core_models.TrainingCall.Status.IN_PROGRESS
                ],
                'page_size': 3
            },
            doseq=True
        )
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.scheduled_seminar_training_call.to_representation(),
            self.scheduled_diplomat_training_call.to_representation(),
            self.in_progress_diplomat_training_call.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data['results'], expected_response)

    def test_retrieve_training_calls_by_tags(self):
        """ Test para validar que se retornen ofertas de formación de las etiquetas especificadas """
        view_url = reverse('api:training-calls')
        query_string = urlencode(
            query={
                'tag': [
                    self.tag_1.slug,
                    self.tag_2.slug
                ],
                'page_size': 3
            },
            doseq=True
        )
        response = self.client.get(f'{view_url}?{query_string}')

        expected_response = [
            self.scheduled_seminar_training_call.to_representation(),
            self.scheduled_diplomat_training_call.to_representation(),
            self.in_progress_diplomat_training_call.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data['results'], expected_response)

    def test_retrieve_latest_training_calls_without_filtering(self):
        """ Test para validar que se obtengan las últimas ofertas de capacitación """
        view_url = reverse('api:latest-training-calls')
        response = self.client.get(view_url)

        expected_response = [
            self.scheduled_seminar_training_call.to_representation(),
            self.scheduled_diplomat_training_call.to_representation(),
            self.in_progress_diplomat_training_call.to_representation(),
            self.in_progress_seminar_training_call.to_representation(),
            self.finished_diplomat_training_call.to_representation(),
            self.finished_seminar_training_call.to_representation()
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_response)
