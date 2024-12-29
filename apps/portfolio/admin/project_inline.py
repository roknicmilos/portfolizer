from django.db import models
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from apps.portfolio.models import Project


class ProjectInline(TranslationStackedInline):
    model = Project
    extra = 0
    classes = ["collapse"]
    verbose_name_plural = _("PROJECTS (R)")
    formfield_overrides = {
        models.CharField: {"widget": Textarea(attrs={"rows": 5, "cols": 74})},
    }

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by(
            models.F("end").asc(nulls_first=True), "-start"
        )
