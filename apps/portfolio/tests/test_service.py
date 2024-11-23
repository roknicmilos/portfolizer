from django.test import TestCase
from django.template.loader import render_to_string
from apps.portfolio import service
from apps.portfolio.models import Portfolio
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
    def test_render_left_column_segments_with_required_data_only(self):
        """
        There shouldn't be any required data for the left column
        which means the returned segment list should be empty.
        """
        portfolio = PortfolioFactory(
            phone=None,
            email=None,
            address_link=None,
            address_label=None,
            birthday=None,
        )

        segments = service.render_left_column_segments(portfolio)

        self.assertEqual(len(segments), 0)

    def test_render_left_column_segments_with_all_data(self):
        """
        Assuming defaults are used, this should be the order
        of the left column segments:
            1. CONTACT
            2. PERSONAL_DETAILS
            3. LINKS
            4. SKILLS
            5. LANGUAGES
            6. INTERNSHIP
            7. EDUCATION
        """
        portfolio = PortfolioFactory()
        LinkFactory(portfolio=portfolio)
        SkillFactory(portfolio=portfolio)
        LanguageFactory(portfolio=portfolio)
        InternshipFactory(portfolio=portfolio)
        EducationFactory(portfolio=portfolio)

        actual_segments = service.render_left_column_segments(portfolio)

        # All six segments should be rendered
        self.assertEqual(len(actual_segments), 7)

        # Check if each expected template is rendered
        expected_segments = [
            self.get_expected_contact_html(portfolio),
            self.get_expected_personal_details_html(portfolio),
            render_to_string(
                template_name="portfolio/includes/links.html",
                context={"links": portfolio.links.all()},
            ),
            render_to_string(
                template_name="portfolio/includes/skills.html",
                context={
                    "skills": portfolio.ordered_skills,
                    "title": "SKILLS",
                },
            ),
            render_to_string(
                template_name="portfolio/includes/skills.html",
                context={
                    "skills": portfolio.languages.all(),
                    "title": "LANGUAGES",
                },
            ),
            render_to_string(
                template_name="portfolio/includes/internship.html",
                context={"internships": portfolio.ordered_internships},
            ),
            render_to_string(
                template_name="portfolio/includes/education.html",
                context={"educations": portfolio.ordered_educations},
            ),
        ]
        self.assertEqual(len(actual_segments), len(expected_segments))
        for index, (actual, expected) in enumerate(
            zip(actual_segments, expected_segments)
        ):
            self.assertEqual(
                first=actual,
                second=expected,
                msg=f"Segment at index {index} does not match",
            )

    def test_render_right_column_segments_with_required_data_only(self):
        portfolio = PortfolioFactory(about_me=None)
        segments = service.render_right_column_segments(portfolio)
        self.assertEqual(len(segments), 0)

    def test_render_right_column_segments_with_all_data(self):
        """
        Assuming defaults are used, this should be the order
        of the right column segments:
            1. ABOUT_ME
            2. EMPLOYMENT
            3. PROJECTS
        """
        portfolio = PortfolioFactory(about_me="About me")
        EmploymentFactory(portfolio=portfolio)
        ProjectFactory(portfolio=portfolio)

        segments = service.render_right_column_segments(portfolio)

        self.assertEqual(len(segments), 3)

        expected_segments = [
            render_to_string(
                template_name="portfolio/includes/about_me.html",
                context={"about_me": portfolio.about_me},
            ),
            render_to_string(
                template_name="portfolio/includes/employment.html",
                context={"employments": portfolio.ordered_employments},
            ),
            render_to_string(
                template_name="portfolio/includes/projects.html",
                context={"projects": portfolio.ordered_projects},
            ),
        ]
        self.assertEqual(segments, expected_segments)

    @staticmethod
    def get_expected_contact_html(portfolio: Portfolio) -> str:
        return render_to_string(
            template_name="portfolio/includes/contact.html",
            context={"contact": portfolio.contact},
        )

    @staticmethod
    def get_expected_personal_details_html(portfolio: Portfolio) -> str:
        return render_to_string(
            template_name="portfolio/includes/personal_details.html",
            context={"personal_details": portfolio.personal_details},
        )
