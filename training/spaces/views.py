# -*- coding: utf-8 -*-
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DeleteView
from django.views.generic.edit import FormView

from training.core.models import State, County
from training.users.mixins import RoleRequiredMixin
from training.users.models import User
from .forms import PhysicalSpaceForm, TrainingSpaceResourceFormSet
from .models import TrainingSpace, TrainingSpaceResource, PhysicalSpace


class PhysicalSpacesDashboardView(RoleRequiredMixin, TemplateView):
    http_method_names = ["get"]
    template_name = "spaces/physical-spaces-dashboard.html"
    allowed_roles = [User.Role.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aggregations = {}
        for type in TrainingSpace.Type.PHYSICAL_TYPES:
            aggregations[type] = Count("pk", filter=Q(type=type))

        stats = PhysicalSpace.objects.aggregate(**aggregations)

        context["stats"] = []
        physical_types_mapper = dict(TrainingSpace.Type.PHYSICAL_CHOICES)
        for type in TrainingSpace.Type.PHYSICAL_TYPES:
            context["stats"].append({"label": physical_types_mapper[type], "count": stats[type]})

        context["breadcrumbs"] = self._get_breadcrumbs()

        return context

    def _get_breadcrumbs(self):
        return [{"href": None, "label": "Módulo de espacios físicos"}]


class PhysicalSpacesListView(RoleRequiredMixin, TemplateView):
    http_method_names = ["get"]
    template_name = "spaces/spaces.html"
    allowed_roles = [User.Role.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = TrainingSpace.Type.PHYSICAL_CHOICES
        context["states"] = State.objects.all().order_by("code")
        context["breadcrumbs"] = self._get_breadcrumbs()
        return context

    def _get_breadcrumbs(self):
        return [
            {"href": reverse("spaces:physical-spaces:dashboard"), "label": "Módulo de espacios físicos"},
            {"href": None, "label": "Espacios físicos"}
        ]


class PhysicalSpaceCUFormView(RoleRequiredMixin, FormView):
    class Action:
        CREATE = "create"
        UPDATE = "update"

    allowed_roles = [User.Role.ADMIN]
    http_method_names = ["get", "post"]
    template_name = "spaces/space.html"
    form_class = PhysicalSpaceForm

    def __init__(self):
        super().__init__()
        self.physical_space = None
        self.physical_space_resource_form_set = None

    def dispatch(self, request, *args, **kwargs):
        training_space_pk = self.kwargs.get("pk")
        if training_space_pk:
            self.physical_space = get_object_or_404(PhysicalSpace, pk=training_space_pk)
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        physical_space_form_params = dict()
        physical_space_resource_form_set_params = dict(prefix="resource")

        if self.request.method == "GET":
            if self.physical_space:
                physical_space_form_params.update(instance=self.physical_space)
                physical_space_resource_form_set_params.update(
                    queryset=self.physical_space.trainingspaceresource_set.all()
                )
            else:
                physical_space_resource_form_set_params.update(queryset=TrainingSpaceResource.objects.none())
        else:
            physical_space_form_params.update(data=self.request.POST)
            physical_space_resource_form_set_params.update(data=self.request.POST)

            if self.physical_space:
                physical_space_form_params.update(instance=self.physical_space)

        physical_space_form = PhysicalSpaceForm(**physical_space_form_params)
        self.physical_space_resource_form_set = TrainingSpaceResourceFormSet(**physical_space_resource_form_set_params)

        return physical_space_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = self.kwargs["action"]
        context["physical_space_resource_form_set"] = self.physical_space_resource_form_set
        context["states"] = [{
            "id": state.id,
            "name": state.name,
            "counties": [{
                "id": county.id,
                "name": county.name
            } for county in County.objects.filter(parent=state).order_by("code")]
        } for state in State.objects.all().order_by("code")]
        context["breadcrumbs"] = self._get_breadcrumbs()

        return context

    def form_valid(self, form):
        physical_space = form.save(commit=False)
        physical_space.save()

        for physical_space_resource_form in self.physical_space_resource_form_set:
            cleaned_data = physical_space_resource_form.cleaned_data
            if physical_space_resource_form.is_valid() and cleaned_data:
                physical_space_resource = physical_space_resource_form.save(commit=False)
                if cleaned_data.get("DELETE"):
                    physical_space_resource.delete()
                else:
                    physical_space_resource.training_space = physical_space
                    physical_space_resource.save()

        return HttpResponseRedirect(reverse("spaces:physical-spaces:all"))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid() and self.physical_space_resource_form_set.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def _get_breadcrumbs(self):
        breadcrumbs = [
            {"href": reverse("spaces:physical-spaces:dashboard"), "label": "Módulo de espacios físicos"},
            {"href": reverse("spaces:physical-spaces:all"), "label": "Espacios físicos"}
        ]

        if self.kwargs["action"] == self.Action.CREATE:
            breadcrumbs.append({"href": None, "label": "Crear"})
        else:
            breadcrumbs.extend([
                {"href": None, "label": self.physical_space.name}, {"href": None, "label": "Modificar"}
            ])

        return breadcrumbs


class TrainingSpaceDeleteView(DeleteView):
    model = TrainingSpace
    success_url = reverse_lazy('spaces:space-list')
