from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from apps.portfolio.models import Portfolio
from apps.portfolio.tests.factories import (
    PortfolioFactory,
    EmploymentFactory,
    InternshipFactory,
    EducationFactory,
    SkillFactory,
    ProjectFactory,
)
from apps.user.tests.factories import UserFactory


class TestPortfolio(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.portfolio = PortfolioFactory()

    def test_str(self):
        self.assertEqual(str(self.portfolio), self.portfolio.title)

    def test_ordered_employments_property(self):
        fist_employment = EmploymentFactory(
            portfolio=self.portfolio,
            start="2019-01-01",
        )
        second_employment = EmploymentFactory(
            portfolio=self.portfolio,
            start="2020-01-01",
        )
        employments = self.portfolio.ordered_employments
        self.assertEqual(len(employments), 2)
        self.assertEqual(employments[0], second_employment)
        self.assertEqual(employments[1], fist_employment)

    def test_ordered_internships_property(self):
        fist_internship = InternshipFactory(
            portfolio=self.portfolio,
            start="2019-01-01",
        )
        second_internship = InternshipFactory(
            portfolio=self.portfolio,
            start="2020-01-01",
        )
        internships = self.portfolio.ordered_internships
        self.assertEqual(len(internships), 2)
        self.assertEqual(internships[0], second_internship)
        self.assertEqual(internships[1], fist_internship)

    def test_ordered_educations_property(self):
        fist_education = EducationFactory(
            portfolio=self.portfolio,
            start="2019-01-01",
        )
        second_education = EducationFactory(
            portfolio=self.portfolio,
            start="2020-01-01",
        )
        educations = self.portfolio.ordered_educations
        self.assertEqual(len(educations), 2)
        self.assertEqual(educations[0], second_education)
        self.assertEqual(educations[1], fist_education)

    def test_ordered_skills_property(self):
        fist_skill = SkillFactory(
            portfolio=self.portfolio,
            level=5,
        )
        second_skill = SkillFactory(
            portfolio=self.portfolio,
            level=1,
        )
        skills = self.portfolio.ordered_skills
        self.assertEqual(len(skills), 2)
        self.assertEqual(skills[0], fist_skill)
        self.assertEqual(skills[1], second_skill)

    def test_ordered_projects_property(self):
        fist_project = ProjectFactory(
            portfolio=self.portfolio,
            start="2019-01-01",
            end="2020-01-01",
        )
        current_project = ProjectFactory(
            portfolio=self.portfolio,
            start="2018-01-01",
            end=None,
        )
        projects = self.portfolio.ordered_projects
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects[0], current_project)
        self.assertEqual(projects[1], fist_project)

    def test_left_column_segment_validation(self):
        # When left column segments are unique,
        # no validation errors should be added:
        self.portfolio.clean()
        self.assertEqual(self.portfolio.validation_errors, {})

        # When left column segments are not unique,
        # validation errors should be added:
        self.portfolio.first_left_segment = self.portfolio.second_left_segment
        with self.assertRaises(ValidationError) as context:
            self.portfolio.clean()
        expected_validation_errors = {
            "first_left_segment": [_("The segment value must be unique.")],
            "second_left_segment": [_("The segment value must be unique.")],
        }
        self.assertEqual(
            context.exception.message_dict, expected_validation_errors
        )

    def test_get_left_segment_order(self):
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
        contact_segment_index = self.portfolio.get_left_segment_order(
            Portfolio.LeftSegment.CONTACT
        )
        personal_details_segment_index = self.portfolio.get_left_segment_order(
            Portfolio.LeftSegment.PERSONAL_DETAILS
        )
        links_segment_index = self.portfolio.get_left_segment_order(
            Portfolio.LeftSegment.LINKS
        )
        skills_segment_index = self.portfolio.get_left_segment_order(
            Portfolio.LeftSegment.SKILLS
        )
        language_segment_index = self.portfolio.get_left_segment_order(
            Portfolio.LeftSegment.LANGUAGES
        )
        internship_segment_index = self.portfolio.get_left_segment_order(
            Portfolio.LeftSegment.INTERNSHIP
        )
        education_segment_index = self.portfolio.get_left_segment_order(
            Portfolio.LeftSegment.EDUCATION
        )

        self.assertEqual(contact_segment_index, 0)
        self.assertEqual(personal_details_segment_index, 1)
        self.assertEqual(links_segment_index, 2)
        self.assertEqual(skills_segment_index, 3)
        self.assertEqual(language_segment_index, 4)
        self.assertEqual(internship_segment_index, 5)
        self.assertEqual(education_segment_index, 6)

    def test_right_column_segment_validation(self):
        # When right column segments are unique,
        # no validation errors should be added:
        self.portfolio.clean()
        self.assertEqual(self.portfolio.validation_errors, {})

        # When right column segments are not unique,
        # validation errors should be added:
        self.portfolio.first_right_segment = self.portfolio.second_right_segment
        with self.assertRaises(ValidationError) as context:
            self.portfolio.clean()
        expected_validation_errors = {
            "first_right_segment": [_("The segment value must be unique.")],
            "second_right_segment": [_("The segment value must be unique.")],
        }
        self.assertEqual(
            context.exception.message_dict, expected_validation_errors
        )

    def test_get_right_segment_order(self):
        """
        Assuming defaults are used, this should be the order
        of the right column segments:
            1. ABOUT_ME
            2. EMPLOYMENT
            3. PROJECTS
        """
        self.assertEqual(
            self.portfolio.get_right_segment_order(
                Portfolio.RightSegment.ABOUT_ME
            ),
            0,
        )
        self.assertEqual(
            self.portfolio.get_right_segment_order(
                Portfolio.RightSegment.EMPLOYMENT
            ),
            1,
        )
        self.assertEqual(
            self.portfolio.get_right_segment_order(
                Portfolio.RightSegment.PROJECTS
            ),
            2,
        )

    def test_portfolio_user_validation(self):
        # When the user is not set, no validation errors should be added:
        self.portfolio.clean()

        # When inactive user is set, validation error should be added:
        user = UserFactory(is_active=False, is_staff=True)
        self.portfolio.update(user=user)
        with self.assertRaises(ValidationError) as context:
            self.portfolio.clean()
        self.assertEqual(
            context.exception.message_dict,
            {"user": [_("Portfolio can't be created for this user.")]},
        )

        # Clear validation errors:
        self.portfolio.validation_errors = {}

        # When non-staff user is set, validation error should be raised:
        user.update(is_active=True, is_staff=False)
        with self.assertRaises(ValidationError) as context:
            self.portfolio.clean()
        self.assertEqual(
            context.exception.message_dict,
            {"user": [_("Portfolio can't be created for this user.")]},
        )

        # Clear validation errors:
        self.portfolio.validation_errors = {}

        # No validation errors should be raised when active staff user has
        # only 1 portfolio:
        user.update(is_active=True, is_staff=True)
        self.portfolio.clean()

        # When staff user has more than 1 portfolio, validation error should
        # be raised:
        PortfolioFactory(user=user)
        with self.assertRaises(ValidationError) as context:
            self.portfolio.clean()
        self.assertEqual(
            context.exception.message_dict,
            {"user": [_("Only one Portfolio can be created for this user.")]},
        )

        # Clear validation errors:
        self.portfolio.validation_errors = {}

        # When superuser has more than 1 portfolio, no validation errors
        # should be raised:
        user.update(is_superuser=True)
        self.portfolio.clean()
        self.assertEqual(self.portfolio.validation_errors, {})

    def test_personal_details_object(self):
        """
        When minimum requirements for PersonalDetails object are met,
        PersonalDetails object should be created.
        """

        # When address_link, address_label and birthday are set,
        # PersonalDetails object should be created:
        portfolio = PortfolioFactory()
        self.assertIsNotNone(portfolio.address_link)
        self.assertIsNotNone(portfolio.address_label)
        self.assertIsNotNone(portfolio.birthday)
        self.assertIsNotNone(portfolio.personal_details)

        # When address_label and birthday are set and address_link is not set,
        # PersonalDetails object should still be created because both birthday
        # and address are available:
        portfolio.update(address_link=None)
        self.assertIsNotNone(portfolio.personal_details)
        self.assertIsNotNone(portfolio.personal_details.address)

        # When address_link and birthday are set and address_label is not set,
        # PersonalDetails object should still be created because birthday is
        # available:
        portfolio.update(address_label=None, address_link="https://example.com")
        self.assertIsNotNone(portfolio.personal_details)
        self.assertIsNone(portfolio.personal_details.address)

        # When address_link and address_label are set and birthday is not set,
        # PersonalDetails object should still be created because address is
        # available:
        portfolio.update(address_label="Address", birthday=None)
        self.assertIsNotNone(portfolio.personal_details)
        self.assertIsNotNone(portfolio.personal_details.address)

        # When address_link, address_label and birthday are not set,
        # PersonalDetails object should not be created:
        portfolio.update(address_link=None, address_label=None)
        self.assertIsNone(portfolio.personal_details)

        # When address_link is set and address_label and birthday are not set,
        # PersonalDetails object should not be created because address and
        # birthday are not available:
        portfolio.update(address_link="https://example.com")
        self.assertIsNone(portfolio.personal_details)

    def test_contact_object(self):
        """
        When minimum requirements for Contact object are met,
        Contact object should be created.
        """

        # When email and phone are not set, Contact object should not be
        # created:
        portfolio = PortfolioFactory(email=None, phone=None)
        self.assertIsNone(portfolio.contact)

        # When email is set and phone is not set, Contact object should be
        # created because email is available:
        portfolio.update(email="example@example.com")
        self.assertIsNotNone(portfolio.contact)

        # When phone is set and email is not set, Contact object should be
        # created because phone is available:
        portfolio.update(email=None, phone="+1 (555) 555-5555")
        self.assertIsNotNone(portfolio.contact)

        # When email and phone are set, Contact object should be created:
        portfolio.update(email="example@example.com")
