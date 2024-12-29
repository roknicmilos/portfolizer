from django.utils.translation import gettext_lazy as _

from apps.portfolio.models import Position


class Employment(Position):
    class Meta:
        verbose_name = _("Employment")
        verbose_name_plural = _("Employments")
        default_related_name = "employments"
        ordering = ["-start"]
