from functools import wraps


def special_registration_view(func):
    """
    Purpose of this decorator is to override the form_invalid method
    of the registration view class. This is done to handle specific
    errors translations in a custom way that couldn't be done in the
    translation files.
    At some point, if the error messages are updated in the translation
    files, this decorator should be removed as it is only a temporary
    solution (workaround).
    """

    @wraps(func)
    def wrapper(cls):
        original_form_invalid = cls.form_invalid

        def new_form_invalid(self, form):
            if form.errors.get("email"):
                for index, error in enumerate(form.errors["email"]):
                    if error == "Korisnik са пољем Email adresa већ постоји.":
                        form.errors["email"][index] = (
                            "Korisnik sa ovom email adresom već postoji."
                        )

            return original_form_invalid(self, form)

        cls.form_invalid = new_form_invalid
        return cls

    return wrapper(func)
