from django.utils.translation import gettext_lazy as _

from apps.portfolio.models import Position


class Internship(Position):
    class Meta:
        verbose_name = _("Internship")
        verbose_name_plural = _("Internships")
        default_related_name = "internships"
        ordering = ["-start"]
