from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from apps.portfolio.models import (
    Education,
    Portfolio,
    Language,
    Position,
    Employment,
    Internship,
    Skill,
    Project,
    Link,
)


class PortfolioFactory(DjangoModelFactory):
    class Meta:
        model = Portfolio

    is_published = Faker("boolean")
    slug = Faker("slug")
    title = Faker("sentence", nb_words=4)
    filename = Faker("file_name", category="image")
    page_count = Faker("random_int", min=1, max=3)
    avatar = None
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    role = Faker("job")
    email = Faker("email")
    phone = "+1 (555) 555-5555"
    address_label = Faker("address")
    address_link = Faker("url")
    birthday = Faker("date_of_birth", minimum_age=18, maximum_age=65)
    about_me = Faker("paragraph")


class EducationFactory(DjangoModelFactory):
    class Meta:
        model = Education

    portfolio = SubFactory(PortfolioFactory)
    school = Faker("company")
    degree = Faker("job")
    start = Faker("date_this_decade")
    end = Faker("date_this_decade", before_today=True, after_today=False)
    location = Faker("city")
    description = Faker("paragraph")


class LanguageFactory(DjangoModelFactory):
    class Meta:
        model = Language

    portfolio = SubFactory(PortfolioFactory)
    label = Faker("language_name")
    level = Faker("random_int", min=1, max=5)


class PositionFactory(DjangoModelFactory):
    class Meta:
        model = Position

    portfolio = SubFactory(PortfolioFactory)
    title = Faker("job")
    company = Faker("company")
    start = Faker("date_this_decade")
    end = Faker("date_this_decade", before_today=True, after_today=False)
    location = Faker("city")
    description = Faker("paragraph")


class EmploymentFactory(PositionFactory):
    class Meta:
        model = Employment


class InternshipFactory(PositionFactory):
    class Meta:
        model = Internship


class SkillFactory(DjangoModelFactory):
    class Meta:
        model = Skill

    portfolio = SubFactory(PortfolioFactory)
    label = Faker("word")
    level = Faker("random_int", min=1, max=5)


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    portfolio = SubFactory(PortfolioFactory)
    name = Faker("sentence", nb_words=4)
    role = Faker("job")
    start = Faker("date_this_decade")
    end = Faker("date_this_decade", before_today=True, after_today=False)
    tools = Faker("words", nb=5, ext_word_list=None, unique=False)
    description = Faker("paragraph")


class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link

    portfolio = SubFactory(PortfolioFactory)
    type = Faker(
        provider="random_element",
        elements=[Link.Type.LINKEDIN, Link.Type.GITHUB, Link.Type.WEBSITE],
    )
    label = Faker("sentence", nb_words=2)
    url = Faker("url")
