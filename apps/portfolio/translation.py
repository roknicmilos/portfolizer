from modeltranslation.translator import TranslationOptions, register

from apps.portfolio.models import (
    Portfolio,
    Employment,
    Internship,
    Education,
    Language,
    Link,
    Project,
    Skill,
)


@register(Portfolio)
class PortfolioTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "filename",
        "role",
        "about_me",
        "address_label",
        # LeftPortfolioColumnMixin fields:
        "contact_segment_title",
        "personal_details_segment_title",
        "links_segment_title",
        "skills_segment_title",
        "languages_segment_title",
        "internship_segment_title",
        "education_segment_title",
        # RightPortfolioColumnMixin fields:
        "about_me_segment_title",
        "employment_segment_title",
        "projects_segment_title",
    )


class PositionTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "company",
        "location",
        "description",
    )


@register(Employment)
class EmploymentTranslationOptions(PositionTranslationOptions):
    pass


@register(Internship)
class InternshipTranslationOptions(PositionTranslationOptions):
    pass


@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = (
        "school",
        "degree",
        "location",
        "description",
    )


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("label",)


@register(Link)
class LinkTranslationOptions(TranslationOptions):
    fields = ("label",)


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "role",
        "tools",
        "tools_title",
        "description",
    )


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = ("label",)
