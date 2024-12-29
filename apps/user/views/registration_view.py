from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.user.decorators import special_registration_view
from apps.user.forms import RegistrationForm


@special_registration_view
class RegistrationView(FormView):
    form_class = RegistrationForm
    success_url = reverse_lazy("admin:index")
    template_name = "user/registration.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: RegistrationForm):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
