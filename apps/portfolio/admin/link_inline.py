from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationTabularInline

from apps.portfolio.models import Link


class LinkInline(TranslationTabularInline):
    model = Link
    extra = 0
    classes = ["collapse"]
    verbose_name_plural = _("LINKS (L)")
