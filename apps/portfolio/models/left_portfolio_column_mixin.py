from django.db import models
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField

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
    contact_segment_title = models.CharField(
        verbose_name=_("contact segment title"),
        max_length=100,
        default=_("CONTACT"),
    )
    personal_details_segment_title = models.CharField(
        verbose_name=_("personal details segment title"),
        max_length=100,
        default=_("PERSONAL DETAILS"),
    )
    links_segment_title = models.CharField(
        verbose_name=_("links segment title"),
        max_length=100,
        default=_("LINKS"),
    )
    skills_segment_title = models.CharField(
        verbose_name=_("skills segment title"),
        max_length=100,
        default=_("SKILLS"),
    )
    languages_segment_title = models.CharField(
        verbose_name=_("languages segment title"),
        max_length=100,
        default=_("LANGUAGES"),
    )
    internship_segment_title = models.CharField(
        verbose_name=_("internship segment title"),
        max_length=100,
        default=_("INTERNSHIP HISTORY"),
    )
    education_segment_title = models.CharField(
        verbose_name=_("education segment title"),
        max_length=100,
        default=_("EDUCATION"),
    )
    left_column_bg_color = ColorField(
        verbose_name=_("left column background color"),
        default="#303030",  # (extra) dark grey
    )
    left_column_text_color = ColorField(
        verbose_name=_("left column text color"),
        default="#ffffff",  # white
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
