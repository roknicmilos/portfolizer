from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _


@deconstructible
class SlugBlacklistValidator(BaseValidator):
    message = _("The slug '%(value)s' is reserved and cannot be used.")
    code = "invalid"
    root_url_paths = [
        "admin",
        "login",
        "logout",
        "register",
        "404",
        "health",
        "i18n",
    ]

    def __init__(self):
        super().__init__(limit_value=None)

    def __call__(self, value):
        if value in self.root_url_paths:
            params = {"value": value}
            raise ValidationError(self.message, code=self.code, params=params)
