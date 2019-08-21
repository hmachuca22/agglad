# -*- coding: utf-8 -*-
from datetime import datetime

from django.urls import reverse
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin

from training.users.models import User
from training.users.mixins import RoleRequiredMixin

from .models import Enrollment, Group, ClassRoom
from training.core.models import TrainingCall
from training.spaces.models import TrainingSpace, PhysicalSpace
from training.users.models import User

from openpyxl import Workbook

class GroupListView(ListView):
    http_method_names = ["get"]
    template_name = "enrollments/groups.html"
    model = Group
    paginate_by = 7

    def get_queryset(self):
        filters = {}
        if self.request.GET.get('filter'):
            filters = {
                'name__icontains':self.request.GET.get('filter')
            }
        if self.request.user.is_admin:
            queryset = Group.objects.filter(**filters).order_by("training_unit__lft")
        else:
            queryset = Group.objects.filter(
                teacher=self.request.user,
                **filters
            ).order_by("training_unit__lft")

        return queryset


class GroupAddView(CreateView):
    template_name = "enrollments/group-form.html"
    model = Group
    fields = [
        "name",
        "modality",
        "teacher",
        "quotas",
        "classes_starts_at",
        "classes_ends_at"
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modality'] = Group.Modality.CHOICES
        context['teachers'] = User.objects.filter(is_teacher=True, is_active=True)
        context['training_call'] = TrainingCall.objects.get(pk=self.kwargs['pk'])
        context['spaces'] = PhysicalSpace.objects.all()
        return context


    def post(self, request, *args, **kwargs):
        teacher_pk = request.POST.get('teacher')
        classes_starts_at = datetime.strptime(request.POST.get('classes_starts_at'),'%d/%m/%Y')
        classes_ends_at = datetime.strptime(request.POST.get('classes_ends_at'),'%d/%m/%Y')

        training_call = TrainingCall.objects.get(pk=self.kwargs['pk'])
        teacher = User.objects.get(pk=teacher_pk)

        group = Group.objects.create(
            name = request.POST.get('name'),
            modality = request.POST.get('modality'),
            teacher = teacher,
            training_call = training_call,
            training_unit = training_call.training_plan,
            quotas = request.POST.get('quotas'),
            classes_starts_at = classes_starts_at,
            classes_ends_at = classes_ends_at
            )
        group.save()

        space = TrainingSpace.objects.get(pk=request.POST.get('space'))
        classroom = ClassRoom.objects.create(
            space=space,
            group= group,
            extra_data = {}
            )
        classroom.save()

        return HttpResponseRedirect(
            reverse('core:training-calls:training-call-detail', kwargs={'slug': training_call.slug})
        )


class GroupUpdateView(UpdateView):
    template_name = "enrollments/group-form.html"
    model = Group
    fields = [
        "name",
        "modality",
        "teacher",
        "quotas",
        "classes_starts_at",
        "classes_ends_at"
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modality'] = Group.Modality.CHOICES
        context['teachers'] = User.objects.filter(is_teacher=True, is_active=True)
        context['training_call'] = TrainingCall.objects.get(pk=self.kwargs['pk'])
        context['spaces'] = TrainingSpace.objects.all()
        return context


    def post(self, request, *args, **kwargs):
        classes_starts_at = datetime.strptime(request.POST.get('classes_starts_at'),'%d/%m/%Y')
        classes_ends_at = datetime.strptime(request.POST.get('classes_ends_at'),'%d/%m/%Y')

        training_call = TrainingCall.objects.get(pk=self.kwargs['pk'])
        teacher = User.objects.get(pk= request.POST.get('teacher'))
        group = Group.objects.get(pk=self.kwargs['pk'])

        group.name = request.POST.get('name')
        group.modality = request.POST.get('modality')
        group.teacher = teacher
        group.training_call = training_call
        group.training_unit = training_call.training_plan
        group.quotas = request.POST.get('quotas')
        group.classes_starts_at = classes_starts_at
        group.classes_ends_at = classes_ends_at

        group.save()
        space = TrainingSpace.objects.get(pk=request.POST.get('space'))
        try:
            classroom = ClassRoom.objects.get(group=group)
        except Exception as e:
            classroom = ClassRoom()
            classroom.group = group
            classroom.extra_data = {}
        
        classroom.space = space
        classroom.save()

        return HttpResponseRedirect(
            reverse('core:training-calls:training-call-detail', kwargs={'slug': training_call.slug})
        )

    def get_success_url(self):
        training_call = TrainingCall.object.get(pk=self.object.training_call.pk)
        return HttpResponseRedirect(
            reverse('core:training-calls:training-call-detail', kwargs={'slug': training_call.slug})
        )


class ClassRoomListView(View):
    def get(self, request):
        return HttpResponse('OK')


class ClassRoomAddView(View):
    def get(self, request):
        return HttpResponse('OK')


class EnrollmentListView(ListView):
    template_name = "enrollments/enrollment.html"
    model = Enrollment

    def get_queryset(self):
        queryset = Enrollment.objects.filter(group__pk=self.kwargs['pk']).order_by('student__full_name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = Group.objects.get(pk=self.kwargs['pk'])
        return context


class EnrollmentAddView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        group = Group.objects.get(pk=request.POST.get('group'))
        try:
            enroll = Enrollment.objects.get(group = group, student = request.user)
        except Exception as e:
            enroll = Enrollment.objects.create(
                group = group,
                student = request.user,
                status = 'reserved'
                )

        return HttpResponseRedirect(reverse('users:self-profile'))


class EnrollmentPrintView(View):
    def get(self, request, *args, **kwargs):
        queryset = Enrollment.objects.filter(
            group__pk = kwargs['pk']
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
                'Ubicación',
                q.group.training_unit.name,
                q.group.training_unit.get_type_display(),
                q.group.training_unit.get_difficulty_level_display(),
                q.group.get_modality_display(),
                q.group.training_unit.duration,
                q.get_status_display()
            ])


        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=matriculados.xlsx'

        wb.save(response)

        return response


class EnrollmentParticipationPrintView(DetailView):
    model = Enrollment
    template_name = "enrollments/participation_print.html"

    def get_queryset(self):
        queryset = Enrollment.objects.filter(
            pk=self.kwargs['pk'],
            status__in=['approved', 'unapproved']
            ).values(
                'group__training_unit__name',
                'group__training_unit__type',
                'group__training_unit__duration',
                'group__classes_starts_at',
                'group__classes_ends_at',
                'group__modality',
                'student__full_name',
                'group__group_classroom__space__type',
                'group__group_classroom__space__name',
                'group__group_classroom__space__organization__name',
                'group__group_classroom__space__location__name'
            )
        return queryset


class EnrollmentHistoryPrintView(ListView):
    model = Enrollment
    template_name = "enrollments/history_print.html"

    def get_queryset(self):
        queryset = Enrollment.objects.filter(
            student__pk=self.kwargs['student'],
            status='approved'
            ).values(
                'group__training_unit__name',
                'group__training_unit__type',
                'group__training_unit__duration',
                'group__classes_starts_at',
                'group__classes_ends_at',
                'group__modality',
                'student__username',
                'student__full_name',
                'group__group_classroom__space__type',
                'group__group_classroom__space__name',
                'group__group_classroom__space__organization__name',
                'group__group_classroom__space__location__name'
            )
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student"] = User.objects.get(pk=self.kwargs['student'])
        return context


class EnrollmentCertificationPrintView(DetailView):
    model = Enrollment
    template_name = "enrollments/certificate_print.html"
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        queryset = Enrollment.objects.filter(
            uuid=self.kwargs['uuid'],
            status='approved'
            ).values(
                'group__training_unit__name',
                'group__training_unit__type',
                'group__training_unit__duration',
                'group__classes_starts_at',
                'group__classes_ends_at',
                'group__modality',
                'student__username',
                'student__full_name',
                'group__group_classroom__space__type',
                'group__group_classroom__space__name',
                'group__group_classroom__space__organization__name',
                'group__group_classroom__space__location__name'
            )
        return queryset
