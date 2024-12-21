from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from apps.portfolio.models import (
    Portfolio,
    Education,
    Employment,
    Internship,
    Language,
    Link,
    Project,
    Skill,
)

from apps.portfolio.models.segments import (
    ContactSegment,
    Segment,
    InternshipSegment,
    EducationSegment,
    LanguagesSegment,
    SkillsSegment,
    LinksSegment,
    PersonalDetailsSegment,
    HeaderSegment,
    AboutMeSegment,
    EmploymentSegment,
    ProjectsSegment,
)


def render_left_column_segments(portfolio: Portfolio) -> list[str]:
    """
    Returns a list of rendered HTML segments for the
    left column of the Portfolio in the order they should be
    displayed which is configured in the Portfolio model.
    """

    segments: list[Segment] = []
    if portfolio.contact:
        segments.append(ContactSegment(portfolio))
    if portfolio.personal_details:
        segments.append(PersonalDetailsSegment(portfolio))
    if portfolio.links.exists():
        segments.append(LinksSegment(portfolio))
    if portfolio.skills.exists():
        segments.append(SkillsSegment(portfolio))
    if portfolio.languages.exists():
        segments.append(LanguagesSegment(portfolio))
    if portfolio.internships.exists():
        segments.append(InternshipSegment(portfolio))
    if portfolio.educations.exists():
        segments.append(EducationSegment(portfolio))

    return [
        segment.content
        for segment in sorted(segments, key=lambda segment: segment.order)
    ]


def render_right_column_segments(portfolio: Portfolio) -> list[str]:
    """
    Returns a list of rendered HTML segments for the
    right column of the Portfolio in the order they should be
    displayed which is configured in the Portfolio model.
    """

    segments: list[Segment] = []
    if portfolio.first_name or portfolio.last_name or portfolio.role:
        segments.append(HeaderSegment(portfolio))
    if portfolio.about_me:
        segments.append(AboutMeSegment(portfolio))
    if portfolio.employments.exists():
        segments.append(EmploymentSegment(portfolio))
    if portfolio.projects.exists():
        segments.append(ProjectsSegment(portfolio))

    return [
        segment.content
        for segment in sorted(segments, key=lambda segment: segment.order)
    ]


def get_default_portfolio_permission() -> list[Permission]:
    allowed_models = [
        Portfolio,
        Education,
        Employment,
        Internship,
        Language,
        Link,
        Project,
        Skill,
    ]

    permissions = []
    for model in allowed_models:
        permissions.extend(_get_model_permissions(model))

    return permissions


def _get_model_permissions(model: type[Model]) -> list[Permission]:
    content_type = ContentType.objects.get_for_model(model)
    return [
        Permission.objects.get(
            codename=f"{permission}_{model._meta.model_name}",
            content_type=content_type,
        )
        for permission in ["view", "add", "change", "delete"]
    ]
