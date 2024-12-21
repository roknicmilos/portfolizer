from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationStackedInline

from apps.portfolio.models import Education


class EducationInline(TranslationStackedInline):
    model = Education
    extra = 0
    classes = ["collapse"]
    verbose_name_plural = _("EDUCATION (L)")
