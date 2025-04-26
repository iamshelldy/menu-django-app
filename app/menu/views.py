from django.shortcuts import render
from django.views import View


class MenuView(View):
    def get(self, request, item_slug: str | None = None):
        return render(request, 'index.html')
