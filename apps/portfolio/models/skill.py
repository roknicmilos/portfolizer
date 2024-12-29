from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Skill(BaseModel):
    portfolio = models.ForeignKey(
        to="Portfolio",
        verbose_name=_("Portfolio"),
        on_delete=models.CASCADE,
        related_name="skills",
    )
    label = models.CharField(
        verbose_name=_("label"),
        max_length=100,
    )
    level = models.PositiveSmallIntegerField(
        verbose_name=_("level"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ["-level", "created"]

    def __str__(self):
        return f"{self.label} ({self.level}/5)"
