# -*- coding: utf-8 -*-
import factory

from training.organizations import factories as organizations_factories
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.sequence(lambda num: str(num).zfill(13))
    first_name = 'John'
    last_name = 'Doe'
    gender = models.User.Gender.MALE
    email = factory.sequence(lambda num: f'email_{num}@training.com')

    class Meta:
        model = models.User


class StudentUserFactory(UserFactory):
    is_student = True


class TeacherUserFactory(UserFactory):
    is_teacher = True


class OrganizationalUserFactory(UserFactory):
    is_organizational = True


class StudentProfileFactory(factory.django.DjangoModelFactory):
    student = factory.SubFactory(StudentUserFactory)

    class Meta:
        model = models.StudentProfile


class TeacherProfileFactory(factory.django.DjangoModelFactory):
    teacher = factory.SubFactory(TeacherUserFactory)

    class Meta:
        model = models.TeacherProfile


class OrganizationalProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(OrganizationalUserFactory)
    organization = factory.SubFactory(organizations_factories.OrganizationFactory)

    class Meta:
        model = models.OrganizationalProfile
