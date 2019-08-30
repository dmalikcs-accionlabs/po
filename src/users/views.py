from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from users.forms import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = CustomLoginForm

    # def form_valid(self, form):
    #     """Security check complete. Log the user in."""
    #     auth_login(self.request, form.get_user())
    #     return HttpResponseRedirect(self.get_success_url())