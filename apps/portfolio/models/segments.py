from abc import ABC, abstractmethod

from django.template.loader import render_to_string

from apps.portfolio.models import Portfolio


class Segment(ABC):
    template_name: str
    order: int
    _bg_color: str
    _text_color: str
    _content: str = None

    @property
    def content(self) -> str:
        if not self._content:
            self._content = self.render_content()
        return self._content

    def render_content(self) -> str:
        return render_to_string(
            template_name=self.template_name,
            context=self.create_context(),
        )

    def create_context(self, **context) -> dict:
        default_context = {
            "bg_color": self._bg_color,
            "text_color": self._text_color,
            "is_last": self.is_last,
        }
        return {**default_context, **context}

    @property
    @abstractmethod
    def is_last(self) -> bool:
        pass


class LeftColumnSegment(Segment):
    def __init__(self, portfolio: Portfolio):
        self._bg_color = portfolio.left_column_bg_color
        self._text_color = portfolio.left_column_text_color

    @property
    def is_last(self) -> bool:
        return self.order == 6


class RightColumnSegment(Segment):
    def __init__(self, portfolio: Portfolio):
        self._bg_color = portfolio.right_column_bg_color
        self._text_color = portfolio.right_column_text_color

    @property
    def is_last(self) -> bool:
        return self.order == 2


class ContactSegment(LeftColumnSegment):
    template_name = ("portfolio/includes/contact.html",)

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.CONTACT
        )
        self._contact = portfolio.contact
        self._title = portfolio.contact_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            contact=self._contact,
            title=self._title,
        )
        return context


class PersonalDetailsSegment(LeftColumnSegment):
    template_name = "portfolio/includes/personal_details.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.PERSONAL_DETAILS
        )
        self._personal_details = portfolio.personal_details
        self._title = portfolio.personal_details_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            personal_details=self._personal_details,
            title=self._title,
        )
        return context


class LinksSegment(LeftColumnSegment):
    template_name = "portfolio/includes/links.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.LINKS
        )
        self._links = portfolio.links.all()
        self._title = portfolio.links_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            links=self._links,
            title=self._title,
        )
        return context


class SkillsSegment(LeftColumnSegment):
    template_name = "portfolio/includes/skills.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.SKILLS
        )
        self._skills = portfolio.skills.all()
        self._title = portfolio.skills_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            skills=self._skills,
            title=self._title,
        )
        return context


class LanguagesSegment(LeftColumnSegment):
    template_name = "portfolio/includes/skills.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.LANGUAGES
        )
        self._skills = portfolio.languages.all()
        self._title = portfolio.languages_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            skills=self._skills,
            title=self._title,
        )
        return context


class InternshipSegment(LeftColumnSegment):
    template_name = "portfolio/includes/internship.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.INTERNSHIP
        )
        self._skills = portfolio.internships.all()
        self._title = portfolio.internship_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            internships=self._skills,
            title=self._title,
        )
        return context


class EducationSegment(LeftColumnSegment):
    template_name = "portfolio/includes/education.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_left_segment_order(
            Portfolio.LeftSegment.EDUCATION
        )
        self._skills = portfolio.educations.all()
        self._title = portfolio.education_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            educations=self._skills,
            title=self._title,
        )
        return context


class HeaderSegment(RightColumnSegment):
    template_name = "portfolio/includes/header.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = -1  # always first
        self._first_name = portfolio.first_name
        self._last_name = portfolio.last_name
        self._role = portfolio.role

    def create_context(self) -> dict:
        context = super().create_context(
            first_name=self._first_name,
            last_name=self._last_name,
            role=self._role,
        )
        return context


class AboutMeSegment(RightColumnSegment):
    template_name = "portfolio/includes/about_me.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_right_segment_order(
            Portfolio.RightSegment.ABOUT_ME
        )
        self._about_me = portfolio.about_me
        self._title = portfolio.about_me_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            about_me=self._about_me,
            title=self._title,
        )
        return context


class EmploymentSegment(RightColumnSegment):
    template_name = "portfolio/includes/employment.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_right_segment_order(
            Portfolio.RightSegment.EMPLOYMENT
        )
        self._employments = portfolio.employments.all()
        self._title = portfolio.employment_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            employments=self._employments,
            title=self._title,
        )
        return context


class ProjectsSegment(RightColumnSegment):
    template_name = "portfolio/includes/projects.html"

    def __init__(self, portfolio: Portfolio):
        super().__init__(portfolio)
        self.order = portfolio.get_right_segment_order(
            Portfolio.RightSegment.PROJECTS
        )
        self._projects = portfolio.ordered_projects
        self._title = portfolio.projects_segment_title

    def create_context(self) -> dict:
        context = super().create_context(
            projects=self._projects,
            title=self._title,
        )
        return context
