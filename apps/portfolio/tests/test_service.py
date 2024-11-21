from django.test import TestCase
from django.template.loader import render_to_string
from apps.portfolio import service
from apps.portfolio.tests.factories import (
    PortfolioFactory,
    LinkFactory,
    SkillFactory,
    LanguageFactory,
    InternshipFactory,
    EducationFactory,
    EmploymentFactory,
    ProjectFactory,
)


class TestService(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.portfolio = PortfolioFactory()
        cls.expected_contact_html = render_to_string(
            template_name="portfolio/includes/contact.html",
            context={
                "address_link": cls.portfolio.address_link,
                "address_label": cls.portfolio.address_label,
                "phone": cls.portfolio.phone,
                "email": cls.portfolio.email,
                "birthday": cls.portfolio.birthday,
            },
        )

    def test_get_left_column_segments_with_required_data_only(self):
        segments = service.get_left_column_segments(self.portfolio)

        self.assertEqual(len(segments), 1)
        self.assertEqual(segments, [self.expected_contact_html])

    def test_get_left_column_segments_with_all_data(self):
        """
        Assuming defaults are used, this should be the order
        of the left column segments:
            1. CONTACT
            2. LINKS
            3. SKILLS
            4. LANGUAGES
            5. INTERNSHIP
            6. EDUCATION
        """
        LinkFactory(portfolio=self.portfolio)
        SkillFactory(portfolio=self.portfolio)
        LanguageFactory(portfolio=self.portfolio)
        InternshipFactory(portfolio=self.portfolio)
        EducationFactory(portfolio=self.portfolio)

        segments = service.get_left_column_segments(self.portfolio)

        # All six segments should be rendered
        self.assertEqual(len(segments), 6)

        # Check if each expected template is rendered
        expected_segments = [
            self.expected_contact_html,
            render_to_string(
                template_name="portfolio/includes/links.html",
                context={"links": self.portfolio.links.all()},
            ),
            render_to_string(
                template_name="portfolio/includes/skills.html",
                context={
                    "skills": self.portfolio.ordered_skills,
                    "title": "SKILLS",
                },
            ),
            render_to_string(
                template_name="portfolio/includes/skills.html",
                context={
                    "skills": self.portfolio.languages.all(),
                    "title": "LANGUAGES",
                },
            ),
            render_to_string(
                template_name="portfolio/includes/internship.html",
                context={"internships": self.portfolio.ordered_internships},
            ),
            render_to_string(
                template_name="portfolio/includes/education.html",
                context={"educations": self.portfolio.ordered_educations},
            ),
        ]
        self.assertEqual(segments, expected_segments)

    def test_get_right_column_segments_with_required_data_only(self):
        self.portfolio.update(about_me=None)
        segments = service.get_right_column_segments(self.portfolio)
        self.assertEqual(len(segments), 0)

    def test_get_right_column_segments_with_all_data(self):
        """
        Assuming defaults are used, this should be the order
        of the right column segments:
            1. ABOUT_ME
            2. EMPLOYMENT
            3. PROJECTS
        """
        self.portfolio.update(about_me="About me")
        EmploymentFactory(portfolio=self.portfolio)
        ProjectFactory(portfolio=self.portfolio)

        segments = service.get_right_column_segments(self.portfolio)

        self.assertEqual(len(segments), 3)

        expected_segments = [
            render_to_string(
                template_name="portfolio/includes/about_me.html",
                context={"about_me": self.portfolio.about_me},
            ),
            render_to_string(
                template_name="portfolio/includes/employment.html",
                context={"employments": self.portfolio.ordered_employments},
            ),
            render_to_string(
                template_name="portfolio/includes/projects.html",
                context={"projects": self.portfolio.ordered_projects},
            ),
        ]
        self.assertEqual(segments, expected_segments)
