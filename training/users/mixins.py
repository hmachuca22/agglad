# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = []

    def get_allowed_roles(self):
        return self.allowed_roles

    def test_func(self):
        user = self.request.user
        if not isinstance(user, AnonymousUser) and user.is_active:
            for role in self.get_allowed_roles():
                print('El rol es-->>', role)
                try:
                    if getattr(user, f"is_{role}", False):
                        return True
                except AttributeError:
                    pass
        return False
