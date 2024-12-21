from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from apps.portfolio.admin import (
    LinkInline,
    SkillInline,
    LanguageInline,
    EducationInline,
    InternshipInline,
    EmploymentInline,
    ProjectInline,
)
from apps.portfolio.models import Portfolio


@admin.register(Portfolio)
class PortfolioAdmin(TranslationAdmin):
    list_display = (
        "title",
        "user",
        "portfolio_link",
        "is_published",
        "created",
        "modified",
    )
    list_filter = ("is_published",)
    search_fields = ("title", "user__email")
    main_fields = (
        "user",
        "is_published",
        "portfolio_link",
        "id",
        "created",
        "modified",
        "slug",
        "title",
        "filename",
        "page_count",
    )
    fieldsets = (
        (
            None,
            {
                "fields": main_fields,
            },
        ),
        (
            _("Left Column | Segment Order"),
            {
                "fields": (
                    "first_left_segment",
                    "second_left_segment",
                    "third_left_segment",
                    "fourth_left_segment",
                    "fifth_left_segment",
                    "sixth_left_segment",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Right Column | Segment Order"),
            {
                "fields": (
                    "first_right_segment",
                    "second_right_segment",
                    "third_right_segment",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Segment Titles"),
            {
                "fields": (
                    "contact_segment_title",
                    "personal_details_segment_title",
                    "links_segment_title",
                    "skills_segment_title",
                    "languages_segment_title",
                    "education_segment_title",
                    "internship_segment_title",
                    "about_me_segment_title",
                    "employment_segment_title",
                    "projects_segment_title",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Style"),
            {
                "fields": (
                    "left_column_bg_color",
                    "left_column_text_color",
                    "right_column_bg_color",
                    "right_column_text_color",
                    "pdf_btn_bg_color",
                    "pdf_btn_svg_color",
                    "edit_btn_bg_color",
                    "edit_btn_svg_color",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("IMAGE (L)"),
            {
                "fields": ("avatar",),
                "classes": ("collapse",),
            },
        ),
        (
            _("CONTACT (L)"),
            {
                "fields": (
                    "email",
                    "phone",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("PERSONAL DETAILS (L)"),
            {
                "fields": (
                    "address_label",
                    "address_link",
                    "birthday",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("HEADER (R)"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "role",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("ABOUT ME (R)"),
            {
                "fields": ("about_me",),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = (
        "id",
        "created",
        "modified",
        "portfolio_link",
    )
    inlines = [
        LinkInline,
        SkillInline,
        LanguageInline,
        EmploymentInline,
        InternshipInline,
        EducationInline,
        ProjectInline,
    ]

    @admin.display(description=_("Portfolio Link"))
    def portfolio_link(self, obj: Portfolio = None) -> str:
        if not obj.pk:
            return _("Save the Portfolio first to generate the link.")

        href = reverse(viewname="portfolio:index", kwargs={"slug": obj.slug})
        label = _("Show portfolio page")
        return mark_safe(f'<a href="{href}">{label}</a>')

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return Portfolio.objects.filter(user=request.user)
        return super().get_queryset(request)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return super().get_list_filter(request)
        return ()

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return super().get_search_fields(request)
        return ()

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return request.user.portfolio_count == 0
        return super().has_add_permission(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user" and not request.user.is_superuser:
            kwargs["queryset"] = db_field.related_model.objects.filter(
                id=request.user.id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["user"] = request.user
        return initial

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        main_fields = fieldsets[0][1]["fields"]
        if not request.user.is_superuser and "user" in main_fields:
            main_fields.remove("user")
        fieldsets[0][1]["fields"] = tuple(main_fields)

        return fieldsets

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        if request.user.is_superuser:
            return super().get_actions(request)
        return ()
