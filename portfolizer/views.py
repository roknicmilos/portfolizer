from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class PageNotFoundView(TemplateView):
    template_name = "404.html"


class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"


class TermsAndConditionsView(TemplateView):
    template_name = "terms_&_conditions.html"
