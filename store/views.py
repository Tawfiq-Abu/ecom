from django.shortcuts import render,get_object_or_404
from django.http import Http404
from .models import Category,Product
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,CreateView,
                                UpdateView,DeleteView)

# Create your views here.
class Homepage(ListView):
    '''
    class item that list all items in the product table and has a queryset 
    funtion to allow it to disply all its info
    
    '''
    model = Product
    context_object_name = 'products'
    template_name = 'store/home.html'

    def get_queryset(self):
        return Product.objects.all

def categories(request):
    '''
    function that returns all objects in the category table 
    in the settings.py we would add "store.views.categories" to the TEMPLATE list under context_processors
    indicating that for every page that we view we have access to the category view
    '''
    return {
        'categories' : Category.objects.all()
    }

class StoreDetail(DetailView):
    model = Product
    template_name = 'store/detail.html'
    context_object_name = 'product'



    '''
    this function checks to see if product is in stock and returns A 404 page is it isn't in stock
    
    '''
    def get_object(self, queryset=None):
        # gets all object in the model provided above
        obj = super().get_object()
        # checks to see if the object in_stock is true or not
        if obj.in_stock != True:
            raise Http404()
        return obj