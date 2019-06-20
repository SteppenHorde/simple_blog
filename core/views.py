from django.shortcuts import render
from django.views.generic.base import TemplateView



class Main(TemplateView):
    template_name = 'core/main.html'
