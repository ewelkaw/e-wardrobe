from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic.edit import View
from ewardrobe_app.forms.register import RegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class UserRegisterView(View):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = "main"
    failure_url = "register"

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})
