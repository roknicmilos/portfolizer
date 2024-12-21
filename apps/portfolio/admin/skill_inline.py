from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationTabularInline

from apps.portfolio.models import Skill


class SkillInline(TranslationTabularInline):
    model = Skill
    extra = 0
    classes = ["collapse"]
    verbose_name_plural = _("SKILLS (R)")
