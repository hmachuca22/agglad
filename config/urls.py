from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from training.core.views import HomeTemplateView, PublicStatsView
from training.users.views import RegisterAccountView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    # Public templates (I assume these are fully API consumers, or should be...)
    path("", HomeTemplateView.as_view(), name="home"),
    path("training/detail/", TemplateView.as_view(template_name="pages/training-detail.html"), name="training-plan-detail"),
    # Expects same template for Login and Sign-up
    path("accounts/login/", LoginView.as_view(template_name="pages/login.html"), name="account_login"),
    path("accounts/logout/", LogoutView.as_view(template_name="pages/logout.html"), name="account_logout"),
    path("accounts/register/", RegisterAccountView.as_view(), name="register_account"),
    path("accounts/password_change/", PasswordChangeView.as_view(template_name="pages/password-change.html"), name="account_password_change"),
    
    # Nuevas urls
    path("accounts/password_change_done/", PasswordChangeDoneView.as_view(template_name='pages/password_change_done.html'), name="password_change_done"),

    path(
        "accounts/password_reset/", 
        PasswordResetView.as_view(
            template_name="account/password_reset.html",
            email_template_name='pages/email_restore.html',
            subject_template_name='account/password_reset_subject.txt',
            success_url="/accounts/password_reset_done/",
            from_email=settings.DEFAULT_FROM_EMAIL
        ),
        name="account_password_reset"
    ),

    path("accounts/password_reset_done/", PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name="account_password_reset_done"),

    path(
        "reset-password/confirm/(P<uidb64>[0-9A-Za-z]+)-(P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/", 
        PasswordResetConfirmView.as_view(
            template_name="pages/password_reset_confirm.html",
            success_url="/reset-password/complete/"
        ),
        name='password_reset_confirm'
    ),

    path("reset-password/complete/", PasswordResetCompleteView.as_view(template_name="pages/password_reset_complete.html"), name='password_reset_complete'),

    path("public/stats/", PublicStatsView.as_view(), name="public_stats"),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    # User management
    path("users/", include("training.users.urls", namespace="users"),),
    # path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("spaces/", include("training.spaces.urls", namespace="spaces"),),
    path("organizations/", include("training.organizations.urls", namespace="organizations"),),
    path("enrollment/", include("training.enrollment.urls", namespace="enrollment"),),
    path("", include("training.core.urls", namespace="core"),),
    path("api/", include("training.api.urls", namespace="api"),),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
