from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationTabularInline

from apps.portfolio.models import Language


class LanguageInline(TranslationTabularInline):
    model = Language
    extra = 0
    classes = ["collapse"]
    verbose_name_plural = _("LANGUAGES (L)")
