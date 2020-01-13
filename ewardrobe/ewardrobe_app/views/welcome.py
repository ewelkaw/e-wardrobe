from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.urls import reverse


class WelcomeView(View):
    template_name = "welcome.html"

    def get(self, request):
        return render(request, self.template_name)
