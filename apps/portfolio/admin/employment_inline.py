from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from apps.portfolio.models import Employment


class EmploymentInline(TranslationStackedInline):
    model = Employment
    extra = 0
    classes = ["collapse"]
    verbose_name_plural = _("EMPLOYMENT (R)")
