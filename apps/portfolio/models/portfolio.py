from apps.common.models import BaseModel
from apps.common.validators import MaxFileSizeValidator
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from apps.portfolio.models import (
    LeftPortfolioColumnMixin,
    RightPortfolioColumnMixin,
)


class Portfolio(LeftPortfolioColumnMixin, RightPortfolioColumnMixin, BaseModel):
    class RightSegment(models.TextChoices):
        ABOUT_ME = "about_me", _("About Me")
        EMPLOYMENT = "employment", _("Employment")
        PROJECTS = "projects", _("Projects")

    user = models.ForeignKey(
        to="user.User",
        verbose_name=_("user"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="portfolios",
    )
    is_published = models.BooleanField(
        verbose_name=_("is published"),
        default=False,
    )
    slug = models.SlugField(
        verbose_name=_("slug"),
        max_length=100,
        unique=True,
    )
    title = models.CharField(
        verbose_name=_("title"),
        max_length=100,
    )
    filename = models.CharField(
        verbose_name=_("filename"),
        max_length=100,
    )
    page_count = models.PositiveSmallIntegerField(
        verbose_name=_("page count"),
        default=1,
        help_text=_(
            "If the content of your Portfolio does not fit on one "
            "page, the content will be automatically split into "
            "multiple pages. Set the expected number of pages here "
            "to apply the first page styling across all pages."
        ),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3),
        ],
    )
    avatar = models.ImageField(
        verbose_name=_("avatar"),
        upload_to="portfolio/images/",
        null=True,
        blank=True,
        validators=[
            MaxFileSizeValidator(100),
        ],
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=50,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=50,
        null=True,
        blank=True,
    )
    role = models.CharField(
        verbose_name=_("role"),
        max_length=100,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_("email"),
        max_length=100,
        null=True,
        blank=True,
    )
    phone = models.CharField(
        verbose_name=_("phone"),
        max_length=20,
        null=True,
        blank=True,
    )
    address_label = models.CharField(
        verbose_name=_("address label"),
        max_length=100,
        null=True,
        blank=True,
    )
    address_link = models.URLField(
        verbose_name=_("address link"),
        max_length=1000,
        null=True,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name=_("birthday"),
        null=True,
        blank=True,
    )
    about_me = models.TextField(
        verbose_name=_("about me"),
        null=True,
        blank=True,
    )
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

    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")

    def __str__(self):
        return self.title

    @property
    def ordered_employments(self) -> models.QuerySet:
        return self.employments.order_by("-start")

    @property
    def ordered_internships(self) -> models.QuerySet:
        return self.internships.order_by("-start")

    @property
    def ordered_educations(self) -> models.QuerySet:
        return self.educations.order_by("-start")

    @property
    def ordered_skills(self) -> models.QuerySet:
        return self.skills.order_by("-level")

    @property
    def ordered_projects(self) -> models.QuerySet:
        return self.projects.order_by(
            models.F("end").asc(nulls_first=True), "-start"
        )

    def clean(self):
        if self.user:
            self._validate_user()
        super().clean()

    def _validate_user(self):
        user_error = None
        if not self.user.is_active or not self.user.is_staff:
            user_error = _("Portfolio can't be created for this user.")
        elif not self.user.is_superuser and self.user.portfolio_count > 1:
            user_error = _("Only one Portfolio can be created for this user.")

        if user_error:
            self.add_validation_error(field_name="user", message=user_error)
