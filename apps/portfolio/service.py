from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.portfolio.models import Portfolio
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


def get_left_column_segments(portfolio: Portfolio) -> list[str]:
    """
    Returns a list of rendered HTML segments for the
    left column of the Portfolio in the order they should be
    displayed which is configured in the Portfolio model.
    """

    segments: list[dict] = []
    if portfolio.contact:
        segments.append({
            "order": portfolio.get_left_segment_order(
                Portfolio.LeftSegment.CONTACT
            ),
            "content": render_to_string(
                template_name="portfolio/includes/contact.html",
                context={"contact": portfolio.contact},
            ),
        })
    if portfolio.personal_details:
        segments.append({
            "order": portfolio.get_left_segment_order(
                Portfolio.LeftSegment.PERSONAL_DETAILS
            ),
            "content": render_to_string(
                template_name="portfolio/includes/personal_details.html",
                context={"personal_details": portfolio.personal_details},
            ),
        })
    if portfolio.links.exists():
        segments.append({
            "order": portfolio.get_left_segment_order(
                Portfolio.LeftSegment.LINKS
            ),
            "content": render_to_string(
                template_name="portfolio/includes/links.html",
                context={"links": portfolio.links.all()},
            ),
        })
    if portfolio.skills.exists():
        segments.append({
            "order": portfolio.get_left_segment_order(
                Portfolio.LeftSegment.SKILLS
            ),
            "content": render_to_string(
                template_name="portfolio/includes/skills.html",
                context={
                    "skills": portfolio.ordered_skills,
                    "title": _("SKILLS"),
                },
            ),
        })
    if portfolio.languages.exists():
        segments.append({
            "order": portfolio.get_left_segment_order(
                Portfolio.LeftSegment.LANGUAGES
            ),
            "content": render_to_string(
                template_name="portfolio/includes/skills.html",
                context={
                    "skills": portfolio.languages.all(),
                    "title": _("LANGUAGES"),
                },
            ),
        })
    if portfolio.internships.exists():
        segments.append({
            "order": portfolio.get_left_segment_order(
                Portfolio.LeftSegment.INTERNSHIP
            ),
            "content": render_to_string(
                template_name="portfolio/includes/internship.html",
                context={"internships": portfolio.ordered_internships},
            ),
        })
    if portfolio.educations.exists():
        segments.append({
            "order": portfolio.get_left_segment_order(
                Portfolio.LeftSegment.EDUCATION
            ),
            "content": render_to_string(
                template_name="portfolio/includes/education.html",
                context={"educations": portfolio.ordered_educations},
            ),
        })

    return [
        segment["content"]
        for segment in sorted(segments, key=lambda x: x["order"])
    ]


def get_right_column_segments(portfolio: Portfolio) -> list[str]:
    """
    Returns a list of rendered HTML segments for the
    right column of the Portfolio in the order they should be
    displayed which is configured in the Portfolio model.
    """

    segments: list[dict] = []
    if portfolio.about_me:
        segments.append({
            "order": portfolio.get_right_segment_order(
                Portfolio.RightSegment.ABOUT_ME
            ),
            "content": render_to_string(
                template_name="portfolio/includes/about_me.html",
                context={"about_me": portfolio.about_me},
            ),
        })
    if portfolio.employments.exists():
        segments.append({
            "order": portfolio.get_right_segment_order(
                Portfolio.RightSegment.EMPLOYMENT
            ),
            "content": render_to_string(
                template_name="portfolio/includes/employment.html",
                context={"employments": portfolio.ordered_employments},
            ),
        })
    if portfolio.projects.exists():
        segments.append({
            "order": portfolio.get_right_segment_order(
                Portfolio.RightSegment.PROJECTS
            ),
            "content": render_to_string(
                template_name="portfolio/includes/projects.html",
                context={"projects": portfolio.ordered_projects},
            ),
        })

    return [
        segment["content"]
        for segment in sorted(segments, key=lambda x: x["order"])
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
