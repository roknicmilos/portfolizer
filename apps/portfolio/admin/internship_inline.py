from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from apps.portfolio.models import Internship


class InternshipInline(TranslationStackedInline):
    model = Internship
    extra = 0
    classes = ["collapse"]
    verbose_name_plural = _("INTERNSHIP (L)")
