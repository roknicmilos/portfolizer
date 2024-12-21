from django.contrib.auth.forms import BaseUserCreationForm

from apps.portfolio import service as portfolio_service
from apps.user import service as user_service

from apps.user.models import User


class RegistrationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

    def save(self, commit=True) -> User:
        self.instance.is_active = True
        self.instance.is_staff = True
        user = self.set_password_and_save(self.instance)
        user.user_permissions.add(
            *user_service.get_default_user_permissions(),
            *portfolio_service.get_default_portfolio_permission(),
        )
        return user
