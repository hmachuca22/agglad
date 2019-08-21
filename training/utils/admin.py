from django.contrib import admin


class CustomBaseAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(CustomBaseAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': self.model._meta.verbose_name_plural}
        return super(CustomBaseAdmin, self).changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin/css/common.css',)
        }
