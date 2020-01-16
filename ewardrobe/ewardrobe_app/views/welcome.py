from django.shortcuts import render
from django.views.generic import View


class WelcomeView(View):
    template_name = "welcome.html"

    def get(self, request):
        return render(request, self.template_name)
