from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.portfolio.models import Portfolio

from apps.portfolio.models.segments import (
    ContactSegment,
    Segment,
    InternshipSegment,
    EducationSegment,
    LanguagesSegment,
    SkillsSegment,
    LinksSegment,
    PersonalDetailsSegment,
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
    content_type = ContentType.objects.get_for_model(Portfolio)

    return [
        Permission.objects.get(
            codename="view_portfolio", content_type=content_type
        ),
        Permission.objects.get(
            codename="add_portfolio", content_type=content_type
        ),
        Permission.objects.get(
            codename="change_portfolio", content_type=content_type
        ),
        Permission.objects.get(
            codename="delete_portfolio", content_type=content_type
        ),
    ]
