from django.contrib import admin
from .models import Code


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'code', 'count', 'get_count_use_code')

    def get_count_use_code(self, obj=None):
        return obj.count_use_code()

    get_count_use_code.short_description = 'Count used'
