from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy


class LoginView(BaseLoginView):
    template_name = "user/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")
