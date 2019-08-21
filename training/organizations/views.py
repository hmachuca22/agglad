# -*- coding: utf-8 -*-
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, TemplateView

from training.core.models import State
from training.users.mixins import RoleRequiredMixin
from training.users.models import User, OrganizationalProfile
from training.users.views import UserCUFormView

from .models import Organization


class OrganizationDashboardView(RoleRequiredMixin, TemplateView):
    http_method_names = ["get"]
    allowed_roles = [User.Role.ADMIN]
    template_name = "organizations/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aggregations = {
            Organization.Type.REGIONAL_CENTER: Count("pk", filter=Q(type=Organization.Type.REGIONAL_CENTER)),
            Organization.Type.DEPARTMENTAL: Count("pk", filter=Q(type=Organization.Type.DEPARTMENTAL)),
            Organization.Type.DISTRICT: Count("pk", filter=Q(type=Organization.Type.DISTRICT)),
            Organization.Type.NGO: Count("pk", filter=Q(type=Organization.Type.NGO)),
        }

        context["stats"] = Organization.objects.aggregate(**aggregations)
        context["breadcrumbs"] = self._get_breadcrumbs()
        return context

    def _get_breadcrumbs(self):
        return [{"href": None, "label": "Módulo de organizaciones"}]


class OrganizationListView(RoleRequiredMixin, TemplateView):
    http_method_names = ['get']
    allowed_roles = [User.Role.ADMIN]
    template_name = "organizations/organizations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = Organization.Type.CHOICES
        context["breadcrumbs"] = self._get_breadcrumbs()
        return context

    def _get_breadcrumbs(self):
        return [
            {"href": reverse("organizations:dashboard"), "label": "Módulo de organizaciones"},
            {"href": None, "label": "Organizaciones"}
        ]


class OrganizationCreateView(CreateView):
    model = Organization
    template_name = "organizations/add_org.html"
    fields = [
        'name',
        'code',
        'type',
    ]
    success_url = reverse_lazy('organizations:organizations')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Organization.Type.CHOICES
        return context


class OrganizationUpdateView(UpdateView):
    model = Organization
    template_name = "organizations/add_org.html"
    fields = [
        'name',
        'code',
        'type',
    ]
    success_url = reverse_lazy('organizations:organizations')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Organization.Type.CHOICES
        return context


class OrganizationDeleteView(DeleteView):
    model = Organization
    # template_name = "organizations/add_org.html"
    success_url = reverse_lazy('organizations:organizations')


# Manage Organizational Users

class OrganizationUsersListView(RoleRequiredMixin, TemplateView):
    http_method_names = ["get"]
    template_name = "organizations/organization_users.html"
    allowed_roles = [User.Role.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genders"] = User.Gender.CHOICES
        context["organization"] = get_object_or_404(Organization, pk=self.kwargs['pk'])
        return context


class OrganizationUserCreateView(UserCUFormView):
    def get_success_url(self):
        return reverse("organizations:organization-user-list", kwargs={"pk": self.kwargs["pk"]})

    def get_organizations(self):
        return Organization.objects.filter(pk=self.kwargs["pk"])


class OrganizationUserTemplateView(TemplateView):
    template_name = "organizations/add_org_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['organization'] = get_object_or_404(Organization, pk=self.kwargs['pk'])
        except Exception as e:
            pass
        return context


class OrganizationUserInactivateView(UpdateView):
    model = OrganizationalProfile

    def post(self, request, *args, **kwargs):
        org_profile = OrganizationalProfile.objects.get(pk=self.kwargs['userpk'])
        org_profile.user.is_active = False
        org_profile.user.save()

        return HttpResponseRedirect(
            reverse('organizations:organization-user-list', kwargs={'pk': self.kwargs['pk']})
        )


class OrganizationUserActivateView(UpdateView):
    model = OrganizationalProfile

    def post(self, request, *args, **kwargs):
        org_profile = OrganizationalProfile.objects.get(pk=self.kwargs['userpk'])
        org_profile.user.is_active = True
        org_profile.user.save()

        return HttpResponseRedirect(
            reverse('organizations:organization-user-list', kwargs={'pk': self.kwargs['pk']})
        )
