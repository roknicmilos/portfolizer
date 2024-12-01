from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class RightPortfolioColumnMixin(BaseModel):
    class RightSegment(models.TextChoices):
        ABOUT_ME = "about_me", _("About Me")
        EMPLOYMENT = "employment", _("Employment")
        PROJECTS = "projects", _("Projects")

    first_right_segment = models.CharField(
        verbose_name=_("first segment in right column"),
        max_length=20,
        choices=RightSegment.choices,
        default=RightSegment.ABOUT_ME,
    )
    second_right_segment = models.CharField(
        verbose_name=_("second segment in right column"),
        max_length=20,
        choices=RightSegment.choices,
        default=RightSegment.EMPLOYMENT,
    )
    third_right_segment = models.CharField(
        verbose_name=_("third segment in right column"),
        max_length=20,
        choices=RightSegment.choices,
        default=RightSegment.PROJECTS,
    )
    about_me_segment_title = models.CharField(
        verbose_name=_("about me segment title"),
        max_length=100,
        default="ABOUT ME",
        null=True,
        blank=True,
    )
    employment_segment_title = models.CharField(
        verbose_name=_("employment segment title"),
        max_length=100,
        default="EMPLOYMENT HISTORY",
        null=True,
        blank=True,
    )
    projects_segment_title = models.CharField(
        verbose_name=_("projects segment title"),
        max_length=100,
        default="RELEVANT PROJECTS",
        null=True,
        blank=True,
    )
    right_column_bg_color = ColorField(
        verbose_name=_("right column background color"),
        default="#ffffff",  # white
    )
    right_column_text_color = ColorField(
        verbose_name=_("right column text color"),
        default="#000000",  # black
    )

    class Meta:
        abstract = True

    def clean(self):
        right_column_segments = {
            "first_right_segment": self.first_right_segment,
            "second_right_segment": self.second_right_segment,
            "third_right_segment": self.third_right_segment,
        }

        duplicates = {
            field_name: value
            for field_name, value in right_column_segments.items()
            if list(right_column_segments.values()).count(value) > 1 and value
        }

        for field_name, value in duplicates.items():
            self.add_validation_error(
                message=_("The segment value must be unique."),
                field_name=field_name,
            )
        super().clean()

    def get_right_segment_order(self, segment: RightSegment) -> int:
        segments = [
            self.first_right_segment,
            self.second_right_segment,
            self.third_right_segment,
        ]
        return segments.index(segment)
