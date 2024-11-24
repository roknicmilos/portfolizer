from abc import ABC

from django.template.loader import render_to_string

from apps.portfolio.models import Portfolio


class Segment(ABC):
    order: int
    content: str
    bg_color: str
    text_color: str


class LeftColumnSegment(Segment):
    def __init__(self, portfolio: Portfolio):
        self.bg_color = portfolio.left_column_bg_color
        self.text_color = portfolio.left_column_text_color


class RightColumnSegment(Segment):
    def __init__(self, portfolio: Portfolio):
        self.bg_color = portfolio.right_column_bg_color
        self.text_color = portfolio.right_column_text_color


class ContactSegment(LeftColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.CONTACT
        )
        self.content = render_to_string(
            template_name="portfolio/includes/contact.html",
            context={
                "contact": portfolio.contact,
                "title": portfolio.contact_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class PersonalDetailsSegment(LeftColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.PERSONAL_DETAILS
        )
        self.content = render_to_string(
            template_name="portfolio/includes/personal_details.html",
            context={
                "personal_details": portfolio.personal_details,
                "title": portfolio.personal_details_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class LinksSegment(LeftColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.LINKS
        )
        self.content = render_to_string(
            template_name="portfolio/includes/links.html",
            context={
                "links": portfolio.links.all(),
                "title": portfolio.links_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class SkillsSegment(LeftColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.SKILLS
        )
        self.content = render_to_string(
            template_name="portfolio/includes/skills.html",
            context={
                "skills": portfolio.ordered_skills,
                "title": portfolio.skills_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class LanguagesSegment(LeftColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.LANGUAGES
        )
        self.content = render_to_string(
            template_name="portfolio/includes/skills.html",
            context={
                "skills": portfolio.languages.all(),
                "title": portfolio.languages_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class InternshipSegment(LeftColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.INTERNSHIP
        )
        self.content = render_to_string(
            template_name="portfolio/includes/internship.html",
            context={
                "internships": portfolio.ordered_internships,
                "title": portfolio.internship_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class EducationSegment(LeftColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.EDUCATION
        )
        self.content = render_to_string(
            template_name="portfolio/includes/education.html",
            context={
                "educations": portfolio.ordered_educations,
                "title": portfolio.education_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class HeaderSegment(RightColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = -1  # always first
        self.content = render_to_string(
            template_name="portfolio/includes/header.html",
            context={
                "first_name": portfolio.first_name,
                "last_name": portfolio.last_name,
                "role": portfolio.role,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class AboutMeSegment(RightColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_right_segment_order(
            Portfolio.RightSegment.ABOUT_ME
        )
        self.content = render_to_string(
            template_name="portfolio/includes/about_me.html",
            context={
                "about_me": portfolio.about_me,
                "title": portfolio.about_me_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class EmploymentSegment(RightColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_right_segment_order(
            Portfolio.RightSegment.EMPLOYMENT
        )
        self.content = render_to_string(
            template_name="portfolio/includes/employment.html",
            context={
                "employments": portfolio.ordered_employments,
                "title": portfolio.employment_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )


class ProjectsSegment(RightColumnSegment):
    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_right_segment_order(
            Portfolio.RightSegment.PROJECTS
        )
        self.content = render_to_string(
            template_name="portfolio/includes/projects.html",
            context={
                "projects": portfolio.ordered_projects,
                "title": portfolio.projects_segment_title,
                "bg_color": self.bg_color,
                "text_color": self.text_color,
            },
        )
