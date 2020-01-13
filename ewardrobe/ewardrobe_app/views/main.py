from django.shortcuts import render
from django.views.generic import View


class MainView(View):
    template_name = "main.html"

    def get(self, request):
        return render(request, self.template_name)
