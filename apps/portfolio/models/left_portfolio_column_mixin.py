from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class LeftPortfolioColumnMixin(BaseModel):
    class LeftSegment(models.TextChoices):
        CONTACT = "contact", _("Contact")
        PERSONAL_DETAILS = "personal_details", _("Personal Details")
        LINKS = "links", _("Links")
        SKILLS = "skills", _("Skills")
        LANGUAGES = "languages", _("Languages")
        INTERNSHIP = "internship", _("Internship")
        EDUCATION = "education", _("Education")

    first_left_segment = models.CharField(
        verbose_name=_("first segment in left column"),
        max_length=20,
        choices=LeftSegment.choices,
        default=LeftSegment.CONTACT,
    )
    second_left_segment = models.CharField(
        verbose_name=_("second segment in left column"),
        max_length=20,
        choices=LeftSegment.choices,
        default=LeftSegment.PERSONAL_DETAILS,
    )
    third_left_segment = models.CharField(
        verbose_name=_("third segment in left column"),
        max_length=20,
        choices=LeftSegment.choices,
        default=LeftSegment.LINKS,
    )
    fourth_left_segment = models.CharField(
        verbose_name=_("fourth segment in left column"),
        max_length=20,
        choices=LeftSegment.choices,
        default=LeftSegment.SKILLS,
    )
    fifth_left_segment = models.CharField(
        verbose_name=_("fifth segment in left column"),
        max_length=20,
        choices=LeftSegment.choices,
        default=LeftSegment.LANGUAGES,
    )
    sixth_left_segment = models.CharField(
        verbose_name=_("sixth segment in left column"),
        max_length=20,
        choices=LeftSegment.choices,
        default=LeftSegment.INTERNSHIP,
    )
    seventh_left_segment = models.CharField(
        verbose_name=_("seventh segment in left column"),
        max_length=20,
        choices=LeftSegment.choices,
        default=LeftSegment.EDUCATION,
    )

    class Meta:
        abstract = True

    def clean(self):
        left_column_segments = {
            "first_left_segment": self.first_left_segment,
            "second_left_segment": self.second_left_segment,
            "third_left_segment": self.third_left_segment,
            "fourth_left_segment": self.fourth_left_segment,
            "fifth_left_segment": self.fifth_left_segment,
            "sixth_left_segment": self.sixth_left_segment,
            "seventh_left_segment": self.seventh_left_segment,
        }

        duplicates = {
            field_name: value
            for field_name, value in left_column_segments.items()
            if list(left_column_segments.values()).count(value) > 1 and value
        }
        for field_name, value in duplicates.items():
            self.add_validation_error(
                message=_("The segment value must be unique."),
                field_name=field_name,
            )

        super().clean()

    def get_left_segment_order(self, segment: LeftSegment) -> int:
        segments = [
            self.first_left_segment,
            self.second_left_segment,
            self.third_left_segment,
            self.fourth_left_segment,
            self.fifth_left_segment,
            self.sixth_left_segment,
            self.seventh_left_segment,
        ]
        return segments.index(segment)
