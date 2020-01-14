from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout
from django.urls import reverse


class UserLogoutView(View):
    template_name = "welcome.html"
    failure_url = "login"

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return render(request, self.template_name)
        else:
            return redirect(reverse(self.failure_url))
