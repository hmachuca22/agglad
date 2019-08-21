# -*- coding: utf-8 -*-
import os
from datetime import date, datetime

from openpyxl import Workbook

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.db.models import Count, Avg, Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, View
from django.views.generic.edit import DeleteView, FormView

from training.enrollment.models import Enrollment, ClassRoom, Group
from training.users.mixins import RoleRequiredMixin
from training.users.models import User

from .forms import TrainingCallForm, TrainingUnitFormset, TrainingCallGroupForm, TrainingCallGroupClassRoomFormset
from .models import Tag, TrainingUnit, PublicLink, Team, Area, GeneralConfiguration, TrainingCall, TrainingUnitTag


class HomeTemplateView(TemplateView):
    template_name="pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.all()

        return context

    
class ContactView(View):
    http_method_names = ["post"]

    def post(self, request):
        general_config = GeneralConfiguration.objects.get()
        options = {
            'question':"Consulta",
            'suggestion':"Sugerencia",
            'appointment':"Cita"
        }
        cause_label = options[request.POST.get('cause')]
        contact_data = {
            'name':request.POST.get('name'),
            'email':request.POST.get('email'),
            'cause': cause_label,
            'message':request.POST.get('message')
        }
        preheader = 'Mensaje de contacto [DGDP]'
        context = {'preheader':preheader, 'contact_data':contact_data}
        template_html = os.path.join(settings.APPS_DIR, 'templates/pages/email_contact.html')
        html_content = render_to_string(template_html, context)
        send_mail('DGDP [Contacto]', '', settings.DEFAULT_FROM_EMAIL,[general_config.contact_email], fail_silently=False, html_message=html_content)
        
        return HttpResponseRedirect(reverse('home'))


class DashboardView(RoleRequiredMixin, TemplateView):
    http_method_names = ["get"]
    template_name = 'core/dashboard.html'
    allowed_roles = User.Role.ALL


class TrainingCallDashboardView(RoleRequiredMixin, TemplateView):
    http_method_names = ["get"]
    allowed_roles = [User.Role.SUPERUSER, User.Role.ADMIN, User.Role.ORGANIZATIONAL]
    template_name = "core/training-call-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self._get_breadcrumbs()

        aggregations = dict()
        for type in TrainingCall.Type.ALL:
            aggregations[f"{type}_total"] = Count("pk", filter=Q(type=type))
            for status in TrainingCall.Status.ALL:
                aggregations[f"{type}_{status}"] = Count("pk", filter=Q(type=type, status=status))

        stats = TrainingCall.objects.aggregate(**aggregations)

        context["stats"] = dict()
        for type in TrainingCall.Type.ALL:
            context["stats"][type] = dict(total=stats[f"{type}_total"])
            for status in TrainingCall.Status.ALL:
                context["stats"][type][status] = stats[f"{type}_{status}"]

        return context

    def _get_breadcrumbs(self):
        return [{"href": None, "label": "Módulo de convocatorias"}]


class TrainingCallListView(TemplateView):
    http_method_names = ["get"]
    template_name = "core/training-calls.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self._get_breadcrumbs()
        context["statuses"], context["show_statuses_filters"] = self._get_statuses_data()
        context["tags"] = self._get_tags()
        return context

    def _get_breadcrumbs(self):
        breadcrumbs = [{"href": None, "label": "Convocatorias"}]

        if not isinstance(self.request.user, AnonymousUser) and (
            self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_organizational
        ):
            breadcrumbs.insert(
                0, {"href": reverse("core:training-calls:dashboard"), "label": "Módulo de convocatorias"}
            )

        return breadcrumbs

    def _get_statuses_data(self):
        statuses_label_mapper = dict(TrainingCall.Status.CHOICES)

        if isinstance(self.request.user, AnonymousUser):
            statuses = [
                {
                    "value": status,
                    "display_name": statuses_label_mapper[status],
                    "selected": True,
                    "hidden": True
                } for status in [
                    TrainingCall.Status.PUBLISHED,
                    TrainingCall.Status.IN_PROGRESS,
                    TrainingCall.Status.CANCELLED,
                    TrainingCall.Status.SUSPENDED,
                    TrainingCall.Status.POSTPONED,
                    TrainingCall.Status.FINISHED
                ]
            ]
            show_statuses_filters = False

        else:
            if self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_organizational:
                statuses = [
                    {
                        "value": status,
                        "display_name": statuses_label_mapper[status],
                        "selected": False,
                        "hidden": False
                    } for status in TrainingCall.Status.ALL
                ]
                show_statuses_filters = True

            else:
                statuses = [
                    {
                        "value": status,
                        "display_name": statuses_label_mapper[status],
                        "selected": True,
                        "hidden": True
                    } for status in [
                        TrainingCall.Status.PUBLISHED,
                        TrainingCall.Status.IN_PROGRESS,
                        TrainingCall.Status.CANCELLED,
                        TrainingCall.Status.SUSPENDED,
                        TrainingCall.Status.POSTPONED,
                        TrainingCall.Status.FINISHED
                    ]
                ]
                show_statuses_filters = False

        return statuses, show_statuses_filters

    def _get_tags(self):
        return tuple(Tag.objects.all().values_list("slug", "display_name").order_by("display_name"))


class TrainingCallCUMixin(RoleRequiredMixin, FormView):  # CU stands for Create and Update
    class Action:
        CREATE = "create"
        UPDATE = "update"

    http_method_names = ['get', 'post']
    allowed_roles = [User.Role.ADMIN, User.Role.ORGANIZATIONAL, User.Role.SUPERUSER]
    success_url = reverse_lazy("core:training-calls:dashboard")

    def __init__(self):
        super().__init__()
        self.training_call = None

    def get(self, request, *args, **kwargs):
        """
        Si la acción a realizar es `UPDATE`, se siguen las siguientes reglas:
        - Las convocatorias con estado `DRAFT` o `REJECTED` solo pueden ser editadas por el usuario que las creo.
        - Las convocatorias con estado `IN_REVISION` solo pueden ser editadas por super usuarios o por el mismo
          usuario que las creo
        - Las convocatorias con estado `APPROVED`, `PUBLISHED`, `IN_PROGRESS`, `CANCELED`, `SUSPENDED`, `POSTPONED`
          o `FINISHED` solo pueden ser editadas por super usuarios
        """
        if self.kwargs["action"] == self.Action.UPDATE:
            if self.training_call.status in [TrainingCall.Status.DRAFT, TrainingCall.Status.REJECTED]:
                if self.training_call.created_by != self.request.user.username:
                    return HttpResponseForbidden()
            elif self.training_call.status == TrainingCall.Status.IN_REVISION:
                if not self.request.user.is_superuser and self.training_call.created_by != self.request.user.username:
                    return HttpResponseForbidden()
            else:
                if not self.request.user.is_superuser:
                    return HttpResponseForbidden()

        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        training_call_form_params = dict(instance=self.training_call)

        if self.request.method == "POST":
            training_call_form_params.update(data=self.request.POST)
            training_call_form_params.update(files=self.request.FILES)

        return TrainingCallForm(**training_call_form_params)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self._get_breadcrumbs()
        context["action"] = self.kwargs["action"]
        context["training_call"] = self.training_call
        context["available_save_actions"] = self._get_available_save_actions()

        return context

    def _get_breadcrumbs(self):
        breadcrumbs = [
            {"href": reverse("core:training-calls:dashboard"), "label": "Módulo de convocatorias"},
            {"href": reverse("core:training-calls:training-calls"), "label": "Convocatorias"},
        ]

        if self.kwargs["action"] == self.Action.CREATE:
            breadcrumbs.append({"href": None, "label": "Crear"})
        else:
            breadcrumbs.extend([
                {
                    "href": reverse(
                        "core:training-calls:training-call-detail",
                        kwargs={
                            "training_call_slug": self.training_call.slug
                        }
                    ),
                    "label": self.training_call.training_plan.name
                }, {
                    "href": None,
                    "label": "Modificar"
                }
            ])

        return breadcrumbs

    def _get_available_save_actions(self):
        available_save_actions = []
        if self.kwargs["action"] == self.Action.CREATE:
            available_save_actions.append({"status": TrainingCall.Status.DRAFT, "action": "Guardar como borrador"})
            if self.request.user.is_superuser:
                available_save_actions.extend([
                    {"status": TrainingCall.Status.APPROVED, "action": "Guardar y aprobar"},
                    {"status": TrainingCall.Status.PUBLISHED, "action": "Guardar y publicar"}
                ])
            else:
                available_save_actions.append(
                    {"status": TrainingCall.Status.IN_REVISION, "action": "Guardar y enviar a revisión"}
                )

        elif self.kwargs["action"] == self.Action.UPDATE:
            if self.training_call.status == TrainingCall.Status.DRAFT:
                available_save_actions.append({"status": TrainingCall.Status.DRAFT, "action": "Guardar cambios"})
                if self.request.user.is_superuser:
                    available_save_actions.extend([
                        {"status": TrainingCall.Status.APPROVED, "action": "Guardar y aprobar"},
                        {"status": TrainingCall.Status.PUBLISHED, "action": "Guardar y publicar"}
                    ])
                else:
                    available_save_actions.append(
                        {"status": TrainingCall.Status.IN_REVISION, "action": "Guardar y enviar a revisión"}
                    )

            elif self.training_call.status == TrainingCall.Status.IN_REVISION:
                if self.request.user.is_superuser:
                    available_save_actions.extend([
                        {"status": TrainingCall.Status.APPROVED, "action": "Aprobar"},
                        {"status": TrainingCall.Status.REJECTED, "action": "Rechazar"},
                        {"status": TrainingCall.Status.PUBLISHED, "action": "Aprobar y publicar"}
                    ])
                else:
                    available_save_actions.extend([
                        {"status": TrainingCall.Status.IN_REVISION, "action": "Guardar cambios"},
                        {"status": TrainingCall.Status.DRAFT, "action": "Guardar como borrador"}
                    ])

            elif self.training_call.status == TrainingCall.Status.APPROVED:
                available_save_actions.extend([
                    {"status": TrainingCall.Status.APPROVED, "action": "Guardar cambios"},
                    {"status": TrainingCall.Status.PUBLISHED, "action": "Guardar y publicar"}
                ])

            elif self.training_call.status == TrainingCall.Status.PUBLISHED:
                available_save_actions.extend([
                    {"status": TrainingCall.Status.PUBLISHED, "action": "Guardar cambios"},
                    {"status": TrainingCall.Status.FINISHED, "action": "Finalizar convocatoria"},
                    {"status": TrainingCall.Status.CANCELLED, "action": "Cancelar convocatoria"}
                ])

            elif self.training_call.status == TrainingCall.Status.IN_PROGRESS:
                available_save_actions.extend([
                    {"status": TrainingCall.Status.IN_PROGRESS, "action": "Guardar cambios"},
                    {"status": TrainingCall.Status.CANCELLED, "action": "Cancelar convocatoria"},
                    {"status": TrainingCall.Status.FINISHED, "action": "Finalizar convocatoria"},
                ])

        return available_save_actions


class SimpleTrainingCallCUView(TrainingCallCUMixin):
    template_name = "core/simple-training-call.html"

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs["action"] == self.Action.UPDATE:
            self.training_call = get_object_or_404(
                TrainingCall, slug=self.kwargs["training_call_slug"], type=TrainingCall.Type.SIMPLE
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        training_plan, _ = TrainingUnit.objects.update_or_create(
            id=int(cleaned_data["training_plan_id"]) if cleaned_data.get("training_plan_id", None) else None,
            defaults=dict(
                name=cleaned_data["training_plan_name"],
                description=cleaned_data["training_plan_description"],
                content=cleaned_data["training_plan_content"],
                difficulty_level=cleaned_data["training_plan_difficulty_level"],
                duration=cleaned_data["training_plan_duration"],
                order=1,
                type=cleaned_data["training_plan_type"],
            )
        )

        training_plan.tags.clear()
        for tag in cleaned_data.get("training_plan_tags"):
            TrainingUnitTag.objects.create(training_unit=training_plan, tag=tag)

        training_call = form.save(commit=False)
        training_call.training_plan = training_plan
        training_call.type = TrainingCall.Type.SIMPLE
        training_call.created_by = self.request.user.username
        training_call.save()

        return HttpResponseRedirect(self.get_success_url())


class CompositeTrainingCallCUView(TrainingCallCUMixin):
    template_name = "core/composite-training-call.html"

    def __init__(self):
        super().__init__()
        self.training_unit_form_set = None

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs["action"] == self.Action.UPDATE:
            self.training_call = get_object_or_404(
                TrainingCall, slug=self.kwargs["training_call_slug"], type=TrainingCall.Type.COMPOSITE
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["training_unit_form_set"] = self.training_unit_form_set
        return context

    def get_form(self, form_class=None):
        # Se agrega el formset encargado de administrar el resto del plan de estudios
        training_unit_form_set_params = dict(prefix="training_unit")
        if self.request.method == "GET":
            if self.training_call:
                training_unit_form_set_params.update(queryset=self.training_call.training_plan.get_descendants())
            else:
                training_unit_form_set_params.update(queryset=TrainingUnit.objects.none())
        else:
            training_unit_form_set_params.update(data=self.request.POST)

        self.training_unit_form_set = TrainingUnitFormset(**training_unit_form_set_params)

        return super().get_form(form_class)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid() and self.training_unit_form_set.is_valid():
            return self.form_valid(form)

        for i in self.training_unit_form_set:
            print(i.errors)
        return self.form_invalid(form)

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        training_plan, _ = TrainingUnit.objects.update_or_create(
            id=int(cleaned_data["training_plan_id"]) if cleaned_data.get("training_plan_id", None) else None,
            defaults=dict(
                name=cleaned_data["training_plan_name"],
                description=cleaned_data["training_plan_description"],
                content=cleaned_data["training_plan_content"],
                difficulty_level=cleaned_data["training_plan_difficulty_level"],
                duration=int(cleaned_data["training_plan_duration"]),
                order=1,
                type=cleaned_data["training_plan_type"],
            )
        )

        training_call = form.save(commit=False)
        training_call.training_plan = training_plan
        training_call.type = TrainingCall.Type.COMPOSITE
        training_call.created_by = self.request.user.username
        training_call.save()

        for training_unit_form in self.training_unit_form_set:
            cleaned_data = training_unit_form.cleaned_data
            if cleaned_data:
                training_unit = training_unit_form.save(commit=False)

                if cleaned_data.get("DELETE"):
                    training_unit.delete()
                else:
                    training_unit.tags.clear()
                    for tag in cleaned_data.get("tags"):
                        TrainingUnitTag.objects.create(training_unit=training_unit, tag=tag)

                    training_unit.parent = training_plan
                    training_unit.save()

        return HttpResponseRedirect(self.get_success_url())


class TrainingCallGroupsView(RoleRequiredMixin, TemplateView):
    http_method_names = ['get', 'post']
    allowed_roles = [User.Role.ADMIN, User.Role.SUPERUSER]
    template_name = "core/training-call-groups.html"

    def __init__(self):
        super().__init__()
        self.training_call = None

    def dispatch(self, request, *args, **kwargs):
        training_call_slug = kwargs["training_call_slug"]
        self.training_call = get_object_or_404(TrainingCall, slug=training_call_slug)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["training_call"] = self.training_call
        context["units"] = self.training_call.training_plan.get_descendants(include_self=True)
        context["breadcrumbs"] = self._get_breadcrumbs()
        return context

    def _get_breadcrumbs(self):
        breadcrumbs = [
            {
                "href": reverse("core:training-calls:dashboard"),
                "label": "Módulo de convocatorias"
            }, {
                "href": reverse("core:training-calls:training-calls"),
                "label": "Convocatorias"
            }, {
                "href": reverse(
                    "core:training-calls:training-call-detail",
                    kwargs={
                        "training_call_slug": self.training_call.slug
                    }
                ),
                "label": self.training_call.training_plan.name
            }, {
                "href": None,
                "label": "Grupos"
            }
        ]

        return breadcrumbs


class TrainingCallCUGroupView(RoleRequiredMixin, FormView):
    class Action:
        CREATE = "create"
        UPDATE = "update"

    http_method_names = ['get', 'post']
    allowed_roles = [User.Role.ADMIN, User.Role.SUPERUSER]
    template_name = "core/training-call-group.html"
    form_class = TrainingCallGroupForm

    def __init__(self):
        super().__init__()
        self.training_call = None
        self.training_unit = None
        self.training_call_group = None
        self.training_call_group_classroom_form_set = None

    def dispatch(self, request, *args, **kwargs):
        self.training_call = get_object_or_404(TrainingCall, slug=self.kwargs["training_call_slug"])
        self.training_unit = get_object_or_404(TrainingUnit, slug=self.kwargs["training_unit_slug"])
        if self.kwargs["action"] == self.Action.UPDATE:
            self.training_call_group = get_object_or_404(
                Group, pk=self.kwargs["group_pk"], training_unit=self.training_unit
            )
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        group_form_params = dict(
            instance=self.training_call_group,
            initial={"training_call": self.training_call, "training_unit": self.training_unit}
        )
        group_classroom_form_set_params = dict(prefix="classroom")

        if self.request.method == "GET":
            if self.kwargs["action"] == self.Action.CREATE:
                group_classroom_form_set_params.update(queryset=ClassRoom.objects.none())
            else:
                group_classroom_form_set_params.update(queryset=self.training_call_group.group_classroom.all())
        else:
            group_form_params.update(data=self.request.POST)
            group_classroom_form_set_params.update(data=self.request.POST)

        self.training_call_group_classroom_form_set = TrainingCallGroupClassRoomFormset(
            **group_classroom_form_set_params
        )

        return TrainingCallGroupForm(**group_form_params)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["training_unit"] = self.training_unit
        context["training_call"] = self.training_call
        context["group"] = self.training_call_group
        context["action"] = self.kwargs["action"]
        context["training_call_group_classroom_form_set"] = self.training_call_group_classroom_form_set
        context["breadcrumbs"] = self._get_breadcrumbs()

        return context

    def form_valid(self, form):
        training_call_group = form.save(commit=False)
        training_call_group.save()

        for training_call_group_classroom_form in self.training_call_group_classroom_form_set:
            cleaned_data = training_call_group_classroom_form.cleaned_data
            if cleaned_data:
                training_call_group_classroom = training_call_group_classroom_form.save(commit=False)
                if cleaned_data.get("DELETE"):
                    training_call_group_classroom.delete()
                else:
                    training_call_group_classroom.group = training_call_group
                    training_call_group_classroom.save()

        return HttpResponseRedirect(
            reverse("core:training-calls:training-call-groups", kwargs=dict(training_call_slug=self.training_call.slug))
        )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid() and self.training_call_group_classroom_form_set.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def _get_breadcrumbs(self):
        breadcrumbs = [
            {
                "href": reverse("core:training-calls:dashboard"),
                "label": "Módulo de convocatorias"
            }, {
                "href": reverse("core:training-calls:training-calls"),
                "label": "Convocatorias"
            }, {
                "href": reverse(
                    "core:training-calls:training-call-detail",
                    kwargs=dict(
                        training_call_slug=self.kwargs["training_call_slug"]
                    )
                ),
                "label": self.training_call.training_plan.name
            }, {
                "href": reverse(
                    "core:training-calls:training-call-groups",
                    kwargs=dict(
                        training_call_slug=self.kwargs["training_call_slug"]
                    )
                ),
                "label": "Grupos"
            }
        ]

        if self.kwargs["action"] == self.Action.CREATE:
            breadcrumbs.append({"href": None, "label": "Agregar"})
        else:
            breadcrumbs.extend([
                {"href": None, "label": self.training_call_group.name},
                {"href": None, "label": "Editar"}
            ])

        return breadcrumbs


class TrainingCallDetailView(TemplateView):
    http_method_names = ["get"]
    template_name = "core/training-call-detail.html"

    def __init__(self):
        super().__init__()
        self.training_call = None

    def dispatch(self, request, *args, **kwargs):
        training_call_slug = kwargs["training_call_slug"]
        self.training_call = get_object_or_404(TrainingCall, slug=training_call_slug)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["training_call"] = self.training_call
        context["breadcrumbs"] = self._get_breadcrumbs()
        return context

    def _get_breadcrumbs(self):
        breadcrumbs = [
            {"href": reverse("core:training-calls:training-calls"), "label": "Convocatorias"},
            {"href": None, "label": self.training_call.training_plan.name}
        ]

        if not isinstance(self.request.user, AnonymousUser) and (
            self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_organizational
        ):
            breadcrumbs.insert(
                0, {"href": reverse("core:training-calls:dashboard"), "label": "Módulo de convocatorias"}
            )

        return breadcrumbs


class PrivateStatsView(TemplateView):
    template_name = "pages/private-stats.html"

    def get_context_data(self, **kwargs):
        if self.request.GET.get('date_from'):
            display_date_from = datetime.strptime(self.request.GET['date_from'], '%d/%m/%Y') 
            display_date_to = datetime.strptime(self.request.GET['date_to'], '%d/%m/%Y') 
        else:
            display_date_from = date(date.today().year, 1, 1)
            display_date_to = date(date.today().year, 12, 31)

        date_args = {
            'group__classes_starts_at__gte': display_date_from,
            'group__classes_starts_at__lte': display_date_to
        }

        tag_args = {}
        unit_tag_args = {}
        area_tag_args = {}
        tag_list = []
        if self.request.GET.get('unit_tags'):
            words = self.request.GET.get('unit_tags').split(',')
            for w in words:
                tag_list.append(w)

            tag_args = {'group__training_unit__tags__slug__in':tag_list}
            unit_tag_args = {'tags__slug__in':tag_list}
            area_tag_args = {'area_user__user_enrollment__group__training_unit__tags__slug__in':tag_list}


        total_enrollment = Enrollment.objects.filter(**date_args, **tag_args).aggregate(students=Count('student'))

        hours_avg = Enrollment.objects.filter(
            status__in=['active', 'approved', 'unapproved'], **date_args, **tag_args
        ).aggregate(hours=Avg('group__training_unit__duration'))

        abandons = Enrollment.objects.filter(
            status__in=['canceled'], **date_args, **tag_args
        ).aggregate(abandons=Count('student'))

        if total_enrollment['students']:
            abandons_per = 100 * abandons['abandons'] / total_enrollment['students']
        else:
            abandons_per = 0

        spaces = ClassRoom.objects.filter(
            group__modality__in=[Group.Modality.FACE_TO_FACE, Group.Modality.COMBINED], **date_args, **tag_args
        ).distinct('space').count()

        spaces_avg = ClassRoom.objects.filter(
            group__modality__in=[Group.Modality.FACE_TO_FACE, Group.Modality.COMBINED], **date_args, **tag_args
        ).aggregate(hours=Avg('group__training_unit__duration'))

        spaces_students = ClassRoom.objects.filter(
            group__modality__in=[Group.Modality.FACE_TO_FACE, Group.Modality.COMBINED], **date_args, **tag_args
        ).aggregate(students=Count('group__group_enrollment__student'))

        if spaces:
            spaces_avg_student = spaces_students['students'] / spaces
        else:
            spaces_avg_student = 0


        training_type_students = TrainingUnit.objects.filter(
            training_unit_group__classes_starts_at__gte=display_date_from,
            training_unit_group__classes_starts_at__lte=display_date_to,
            **unit_tag_args
        ).values('type'
                 ).annotate(
            students=Count('training_unit_group__group_enrollment__student')
        ).order_by('type')

        training_level_students = TrainingUnit.objects.filter(
            training_unit_group__classes_starts_at__gte=display_date_from,
            training_unit_group__classes_starts_at__lte=display_date_to,
            **unit_tag_args
        ).values('difficulty_level'
                 ).annotate(
            students=Count('training_unit_group__group_enrollment__student')
        ).order_by('difficulty_level')

        hours_area = (
            Area.objects.filter(
                area_user__user_enrollment__group__classes_starts_at__gte = display_date_from,
                area_user__user_enrollment__group__classes_starts_at__lte = display_date_to,
                **area_tag_args
            )
            .values('name')
            .annotate(
                students=Count('area_user__user_enrollment'),
                hours=Avg('area_user__user_enrollment__group__training_unit__duration'),
            )
            .order_by('name')
        )

        context = super().get_context_data(**kwargs)
        context['total_enrollment'] = total_enrollment
        context['hours_avg'] = hours_avg
        context['abandons'] = abandons_per
        context['spaces'] = spaces
        context['spaces_avg'] = spaces_avg
        context['spaces_avg_student'] = spaces_avg_student
        context['training_type_students'] = training_type_students
        context['training_level_students'] = training_level_students
        context['hours_area'] = hours_area
        context['tags'] = Tag.objects.all()
        context['display_date_from'] = display_date_from
        context['display_date_to'] = display_date_to
        context['display_tags'] = tag_list

        return context


class DesertersListView(TemplateView):
    template_name = "reports/list-deserters.html"

    def get_context_data(self, **kwargs):
        if self.request.GET.get('date_from'):
            display_date_from = datetime.strptime(self.request.GET['date_from'], '%d/%m/%Y') 
            display_date_to = datetime.strptime(self.request.GET['date_to'], '%d/%m/%Y') 
        else:
            display_date_from = date(date.today().year, 1, 1)
            display_date_to = date(date.today().year, 12, 31)

        tag_args = {}
        area_tag_args = {}
        group_tag_args = {}
        tag_list = []
        if self.request.GET.get('unit_tags'):
            words = self.request.GET.get('unit_tags').split(',')
            for w in words:
                tag_list.append(w)

            tag_args = {'group__training_unit__tags__slug__in':tag_list}
            group_tag_args = {'training_unit__tags__slug__in':tag_list}
            area_tag_args = {'area_user__user_enrollment__group__training_unit__tags__slug__in':tag_list}

        abandons = Enrollment.objects.filter(
            group__classes_starts_at__gte=display_date_from,
            group__classes_starts_at__lte=display_date_to,
            status__in=['canceled'],
            **tag_args
        ).values(
            'student__first_name',
            'student__last_name',
            'student__email',
            'group__training_unit__name',
            'group__training_unit__type',
            'group__modality',
            'student__residence_place__name',
        )

        modality_abandons = Group.objects.filter(
            classes_starts_at__gte=display_date_from,
            classes_starts_at__lte=display_date_to,
            group_enrollment__status='canceled',
            **group_tag_args
        ).values('modality'
                 ).annotate(
            students=Count('group_enrollment__student')
        ).order_by('modality')


        states = (
            Area.objects.filter(
                area_user__user_enrollment__group__classes_starts_at__gte=display_date_from,
                area_user__user_enrollment__group__classes_starts_at__lte=display_date_to,
                type=Area.Type.STATE,
                area_user__user_enrollment__status='canceled',
                **area_tag_args
            )
            .values('name')
            .annotate(students=Count('area_user__user_enrollment'))
            .order_by('name')
        )

        context = super().get_context_data(**kwargs)
        context['object_list'] = abandons
        context['modality_abandons'] = modality_abandons
        context['states'] = states
        context['tags'] = Tag.objects.all()
        context['display_date_from'] = display_date_from
        context['display_date_to'] = display_date_to
        context['display_tags'] = tag_list

        return context


class EmployeeTypesView(TemplateView):
    template_name = "reports/employee_type.html"

    def get_context_data(self, **kwargs):
        if self.request.GET.get('date_from'):
            display_date_from = datetime.strptime(self.request.GET['date_from'], '%d/%m/%Y') 
            display_date_to = datetime.strptime(self.request.GET['date_to'], '%d/%m/%Y') 
        else:
            display_date_from = date(date.today().year, 1, 1)
            display_date_to = date(date.today().year, 12, 31)

        tag_args = {}
        tag_list = []
        if self.request.GET.get('unit_tags'):
            words = self.request.GET.get('unit_tags').split(',')
            for w in words:
                tag_list.append(w)

            tag_args = {'group__training_unit__tags__slug__in':tag_list}

        result_list = Enrollment.objects.filter(
            group__classes_starts_at__gte=display_date_from,
            group__classes_starts_at__lte=display_date_to,
            **tag_args
            ).values(
            'student__employee_type__type',
            'student__employee_type__name',
            'student__residence_place__name',
            'group__training_unit__type',
            'group__modality',
            'status'
            ).annotate(students=Count('student', distinct=True)
            ).order_by(
            'student__employee_type__type',
            'student__employee_type__name',
            'student__residence_place__name',
            'group__training_unit__type',
            'group__modality',
            'status')

        context = super().get_context_data(**kwargs)
        context['result_list'] = result_list
        context['tags'] = Tag.objects.all()
        context['display_date_from'] = display_date_from
        context['display_date_to'] = display_date_to
        context['display_tags'] = tag_list

        return context


class ParticipantsView(TemplateView):
    template_name = "reports/participants.html"

    def get_context_data(self, **kwargs):
        if self.request.GET.get('date_from'):
            display_date_from = datetime.strptime(self.request.GET['date_from'], '%d/%m/%Y') 
            display_date_to = datetime.strptime(self.request.GET['date_to'], '%d/%m/%Y') 
        else:
            display_date_from = date(date.today().year, 1, 1)
            display_date_to = date(date.today().year, 12, 31)

        tag_args = {}
        area_tag_args = {}
        user_tag_args = {}
        unit_tag_args = {}
        tag_list = []
        if self.request.GET.get('unit_tags'):
            words = self.request.GET.get('unit_tags').split(',')
            for w in words:
                tag_list.append(w)

            tag_args = {'group__training_unit__tags__slug__in':tag_list}
            area_tag_args = {'area_user__user_enrollment__group__training_unit__tags__slug__in':tag_list}
            user_tag_args = {'user_enrollment__group__training_unit__tags__slug__in':tag_list}
            unit_tag_args = {'tags__slug__in':tag_list}

        states = (
            Area.objects.filter(
                area_user__user_enrollment__group__classes_starts_at__gte=display_date_from,
                area_user__user_enrollment__group__classes_starts_at__lte=display_date_to,
                type=Area.Type.STATE,
                **area_tag_args
            )
            .values('name')
            .annotate(students=Count('area_user__user_enrollment'))
            .order_by('name')
        )


        users = User.objects.filter(
            user_enrollment__group__classes_starts_at__gte=display_date_from,
            user_enrollment__group__classes_starts_at__lte=display_date_to,
            **user_tag_args
            ).order_by('-birth_day')

        ages = []
        for u in users:
            ages.append(u.age)

        ages_list = set(ages)

        user_dict = []
        for age in sorted(ages_list):
            males = 0
            females = 0
            other = 0
            for user in users:
                if age == user.age:
                    if user.gender == 'male':
                        males += 1
                    elif user.gender == 'female':
                        females += 1
                    else:
                        other += 1

            total = males + females + other

            user_dict.append({'age': age, 'males': males, 'females': females, 'other': other, 'total':total})


        type_modality_students = TrainingUnit.objects.filter(
            training_unit_group__classes_starts_at__gte=display_date_from,
            training_unit_group__classes_starts_at__lte=display_date_to,
            **unit_tag_args
        ).values('type', 'training_unit_group__modality'
                 ).annotate(
            students=Count('training_unit_group__group_enrollment__student')
        ).order_by('type', 'training_unit_group__modality')

        participants = Enrollment.objects.filter(
            group__classes_starts_at__gte=display_date_from,
            group__classes_starts_at__lte=display_date_to,
            **tag_args
        ).order_by('student__full_name')

        context = super().get_context_data(**kwargs)
        context['states'] = states
        context['users_age'] = user_dict
        context['type_modality_students'] = type_modality_students
        context['participants'] = participants
        context['tags'] = Tag.objects.all()
        context['display_date_from'] = display_date_from
        context['display_date_to'] = display_date_to
        context['display_tags'] = tag_list

        return context


class ParticipantsExportView(View):
    def get(self, request):
        if self.request.GET.get('date_from'):
            display_date_from = datetime.strptime(self.request.GET['date_from'], '%d/%m/%Y') 
            display_date_to = datetime.strptime(self.request.GET['date_to'], '%d/%m/%Y') 
        else:
            display_date_from = date(date.today().year, 1, 1)
            display_date_to = date(date.today().year, 12, 31)

        queryset = Enrollment.objects.filter(
            group__classes_starts_at__gte=display_date_from,
            group__classes_starts_at__lte=display_date_to
        ).order_by('student__full_name')

        wb = Workbook(write_only=True)
        ws = wb.create_sheet()

        ws.append([
            'Nombre',
            'Identidad',
            'Género',
            'Fecha de Nacimiento',
            'Edad',
            'Procedencia',
            'Capacitación',
            'Tipo Capacitación',
            'Nivel de Dificultad',
            'Modalidad',
            'Duración (Hrs)',
            'Estado de Matrícula'
        ])

        for q in queryset:
            ws.append([
                q.student.full_name,
                q.student.username,
                q.student.get_gender_display(),
                q.student.birth_day,
                q.student.age,
                q.student.residence_place.name,
                q.group.training_unit.name,
                q.group.training_unit.get_type_display(),
                q.group.training_unit.get_difficulty_level_display(),
                q.group.get_modality_display(),
                q.group.training_unit.duration,
                q.get_status_display()
            ])


        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=base_matriculados.xlsx'

        wb.save(response)

        return response


class PublicStatsView(TemplateView):
    template_name = "pages/public-stats.html"

    def get_context_data(self, **kwargs):
        enrollment = Enrollment.objects.filter(
            group__classes_starts_at__gte=date(date.today().year, 1, 1),
            group__classes_starts_at__lte=date(date.today().year, 12, 31)
            )

        total_enrollment = enrollment.aggregate(students=Count('student'))

        hours_avg = enrollment.filter(
            status__in=['active', 'approved', 'unapproved']
            ).aggregate(hours=Avg('group__training_unit__duration'))

        states = Area.objects.filter(
            area_user__user_enrollment__group__classes_starts_at__gte=date(date.today().year, 1, 1),
            area_user__user_enrollment__group__classes_starts_at__lte=date(date.today().year, 12, 31),
            type='state'
            ).values('name'
            ).annotate(students=Count('area_user__user_enrollment__group__group_enrollment__student')
            ).order_by('name')

        users = User.objects.filter(
            user_enrollment__group__classes_starts_at__gte=date(date.today().year, 1, 1),
            user_enrollment__group__classes_starts_at__lte=date(date.today().year, 12, 31)
            ).order_by('-birth_day')

        ages = []
        for u in users:
            ages.append(u.age)

        ages_list = set(ages)

        user_dict = []
        for age in sorted(ages_list):
            students = 0
            for user in users:
                if age == user.age:
                    students += 1

            user_dict.append({'age':age, 'students': students})

        training_type_students = TrainingUnit.objects.filter(
            training_unit_group__classes_starts_at__gte=date(date.today().year, 1, 1),
            training_unit_group__classes_starts_at__lte=date(date.today().year, 12, 31)
            ).values('type'
            ).annotate(
                students=Count('training_unit_group__group_enrollment__student')
            ).order_by('type')

        context = super().get_context_data(**kwargs)
        context['total_enrollment'] = total_enrollment
        context['hours_avg'] = hours_avg
        context['states'] = states
        context['students'] = user_dict
        context['training_type_students'] = training_type_students
        context['display_date_from'] = date(date.today().year, 1, 1)
        context['display_date_to'] = date(date.today().year, 12, 31)

        return context


# Public Links
class PublicLinksListView(ListView):
    model = PublicLink
    template_name = "links/list-public-links.html"


class PublicLinksCreateView(CreateView):
    model = PublicLink
    template_name = "links/add-public-links.html"
    fields = [
        'name',
        'url_path',
    ]
    success_url = reverse_lazy('core:list-public-links')


class PublicLinksUpdateView(UpdateView):
    model = PublicLink
    template_name = "links/add-public-links.html"
    fields = [
        'name',
        'url_path',
    ]
    success_url = reverse_lazy('core:list-public-links')


class PublicLinksDeleteView(DeleteView):
    model = PublicLink
    success_url = reverse_lazy('core:list-public-links')


# Team
class TeamListView(ListView):
    model = Team
    template_name = "team/team-list.html"


class TeamCreateView(CreateView):
    model = Team
    template_name = "team/team-add.html"
    fields = [
        'user',
        'position',
        'photo',
    ]
    success_url = reverse_lazy('core:team')

    def get_context_data(self, **kwargs):
        team_members = Team.objects.all().values('user')
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(is_organizational=True).exclude(pk__in=team_members)
        return context


class TeamUpdateView(UpdateView):
    model = Team
    template_name = "team/team-add.html"
    fields = [
        'user',
        'position',
        'photo',
    ]
    success_url = reverse_lazy('core:team')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(is_organizational=True)
        return context


class TeamDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy('core:team')



