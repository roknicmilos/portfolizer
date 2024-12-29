from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Education(BaseModel):
    portfolio = models.ForeignKey(
        to="Portfolio",
        verbose_name=_("Portfolio"),
        on_delete=models.CASCADE,
        related_name="educations",
    )
    school = models.CharField(
        verbose_name=_("school"),
        max_length=100,
    )
    degree = models.CharField(
        verbose_name=_("degree"),
        max_length=100,
    )
    start = models.DateField(
        verbose_name=_("start"),
        help_text=_(
            "Day is not important. Select 1st if you don't "
            "know the exact start day."
        ),
    )
    end = models.DateField(
        verbose_name=_("end"),
        null=True,
        blank=True,
        help_text=_(
            "Leave empty if you are currently studying here. "
            "Day is not important. Select 1st if you don't "
            "know the exact end day."
        ),
    )
    location = models.CharField(
        verbose_name=_("location"),
        max_length=100,
    )
    description = models.TextField(
        verbose_name=_("description"),
    )

    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Educations")
        ordering = ["-start"]

    def __str__(self):
        return f"{self.school} - {self.degree}"

    @property
    def title(self):
        return str(self)
