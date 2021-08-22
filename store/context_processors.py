
from .models import Category

def categories(request):
    '''
    function that returns all objects in the category table 
    in the settings.py we would add "store.views.categories" to the TEMPLATE list under context_processors
    indicating that for every page that we view we have access to the category view
    '''
    return {
        'categories' : Category.objects.all()
    }