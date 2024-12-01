from django.http import Http404
from django.middleware.csrf import get_token
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django_pdf_view.pdf import PDF
from django_pdf_view.views import PDFView

from apps.common.utils import get_model_admin_details_url
from apps.portfolio.models import Portfolio
from apps.portfolio import service


class PortfolioPDFView(PDFView):
    portfolio: Portfolio
    template_name = "portfolio/portfolio_content.html"
    css_paths = ["portfolio/css/portfolio/"]

    def create_pdf(self) -> PDF:
        self.portfolio = self._get_portfolio()
        return PDF(
            template_name=self.template_name,
            base_template_name="portfolio/portfolio.html",
            title=self.portfolio.title,
            filename=self.portfolio.filename,
            context=self.get_context(),
            css_paths=self.css_paths.copy(),
        )

    def get_context(self) -> dict:
        context = super().get_context()
        context["portfolio"] = self.portfolio
        context["avatar_url"] = self._get_absolut_avatar_url()
        context["left_column"] = service.render_left_column_segments(
            portfolio=self.portfolio
        )
        context["right_column"] = service.render_right_column_segments(
            portfolio=self.portfolio
        )

        if self.response_type == "html":
            context.update(self._get_html_context())

        return context

    def _get_html_context(self) -> dict:
        portfolio_pdf_url = reverse(
            viewname="portfolio:pdf", kwargs={"slug": self.portfolio.slug}
        )
        context = {
            "portfolio_pdf_url": portfolio_pdf_url,
            "csrf_token": get_token(self.request),
        }
        if self.portfolio.user == self.request.user:
            context["portfolio_edit_url"] = get_model_admin_details_url(
                obj=self.portfolio
            )
        return context

    def _get_portfolio(self) -> Portfolio:
        portfolio = get_object_or_404(klass=Portfolio, slug=self.kwargs["slug"])

        if not portfolio.is_published and self.request.user != portfolio.user:
            raise Http404

        return portfolio

    def _get_absolut_avatar_url(self) -> str:
        if self.portfolio.avatar:
            return self.request.build_absolute_uri(self.portfolio.avatar.url)
        return ""
