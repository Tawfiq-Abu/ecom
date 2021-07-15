from django.shortcuts import render
from .models import Category,Product
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,CreateView,
                                UpdateView,DeleteView)

# Create your views here.
class Homepage(ListView):
    model = Product
    template_name = 'store/home.html'

    def get_queryset(self):
        return Product.objects.all