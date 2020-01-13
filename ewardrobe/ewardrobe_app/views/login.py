from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import View
from ewardrobe_app.forms.login import UserLoginForm
from django.urls import reverse


class UserLoginView(View):
    template_name = "login.html"
    form_class = UserLoginForm
    success_url = "main"
    failure_url = "welcome"

    def post(self, request):
        username = request.POST.get("username")
        raw_password = request.POST.get("password")
        user = authenticate(username=username, password=raw_password)

        if user is not None:
            login(request, user)
            return redirect(reverse(self.success_url))
        else:
            return redirect(reverse(self.failure_url))

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {"form": form})
