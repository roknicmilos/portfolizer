from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.utils.translation import gettext_lazy as _

from apps.portfolio import service as portfolio_service
from apps.user import service as user_service

from apps.user.models import User


class RegistrationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

    has_accepted_terms_and_policy = forms.BooleanField(
        required=True,
        label=_(
            "I agree to the Terms & Conditions and "
            "acknowledge the Privacy Policy."
        ),
        help_text=_(
            "Please read and accept the Terms & Conditions and "
            "Privacy Policy before proceeding. You can find them "
            "by clicking the links in the footer."
        ),
    )

    def save(self, commit=True) -> User:
        self.instance.is_active = True
        self.instance.is_staff = True
        user = self.set_password_and_save(self.instance)
        user.user_permissions.add(
            *user_service.get_default_user_permissions(),
            *portfolio_service.get_default_portfolio_permission(),
        )
        return user
