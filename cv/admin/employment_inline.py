from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from cv.models import Employment


class EmploymentInline(admin.StackedInline):
    model = Employment
    extra = 0
    classes = ['collapse']
    verbose_name_plural = _('EMPLOYMENT (R)')