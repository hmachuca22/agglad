# -*- coding: utf-8 -*-
from django.urls import reverse

from training.core.models import PublicLink, GeneralConfiguration


def custom_context(request):
    context = {}
    public_links = PublicLink.objects.all()
    context.update({'public_links': public_links})
    try:
        general_config = GeneralConfiguration.objects.get()
        context.update({'general_config': general_config})
    except Exception as e:
        pass

    if request.user.is_authenticated:
        context["menu_sections"] = []
        if request.user.is_admin or request.user.is_teacher or request.user.is_organizational:
            administration_section = {
                "name": "Administración",
                "icon": "psi-gear-2",
                "items": []
            }

            if request.user.is_admin:
                administration_section["items"].extend([
                    {
                        "name": "Usuarios",
                        "url": reverse("users:dashboard")
                    }, {
                        "name": "Convocatorias",
                        "url": reverse("core:training-calls:dashboard")
                    }, {
                        "name": "Organizaciones",
                        "url": reverse("organizations:dashboard")
                    }, {
                        "name": "Espacios Físicos",
                        "url": reverse("spaces:physical-spaces:dashboard")
                    }, {
                        "name": "Equipo de Trabajo",
                        "url": reverse("core:team")
                    }
                ])
            else:
                if request.user.is_organizational:
                    administration_section["items"].append({
                        "name": "Convocatorias",
                        "url": reverse("core:training-calls:dashboard")
                    })

            if request.user.is_teacher:
                administration_section["items"].extend([
                    {
                        "divider": True
                    }, {
                        "name": "Grupos Asignados",
                        "url": reverse("enrollment:group-list")
                    }
                ])

            context["menu_sections"].append(administration_section)

        if request.user.is_student:
            enrollments_section = {
                "name": "Mis matrículas",
                "icon": "psi-bookmark",
                "items": []  # TODO: Obtener cursos actuales
            }

            context["menu_sections"].append(enrollments_section)

        context["menu_sections"].append({
            "name": "Estadísticas",
            "icon": "psi-bar-chart",
            "items": [
                {
                    "name": "Globales",
                    "url": reverse("core:stats")
                }, {
                    "name": "Participación",
                    "url": reverse("core:participants")
                }, {
                    "name": "Tipo de empleado",
                    "url": reverse("core:employee-types")
                }, {
                    "name": "Deserción",
                    "url": reverse("core:deserters")
                }
            ]
        })

    return context
