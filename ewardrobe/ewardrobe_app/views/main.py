from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse


class MainView(View):
    template_name = "main.html"
    failure_url = "login"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect(reverse(self.failure_url))
