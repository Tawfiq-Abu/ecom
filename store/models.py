from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.



# Create your models here.
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager,self).get_queryset().filter(is_active=True)




class Category(models.Model):
    name = models.CharField(max_length=256,db_index=True)
    # eg. www.facebook.com/profile the profile is the slug
    slug = models.SlugField(max_length=256,unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("store:category_list", kwargs={"slug": self.slug})
    
        
    class Meta:
        # this when categories are more than one would set the db model name to be categories instead of category
        verbose_name_plural = 'categories'

class Product(models.Model):
    Category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, related_name = 'uploader', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    slug = models.SlugField(max_length=256,unique=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        # django automatically adds 's' to the model name so this isn't really needed
        verbose_name_plural = 'Products'
        ordering = ('-uploaded',)

    def __str__(self):
            return self.name

    # dynamic urls
    def get_absolute_url(self):
        # you can use args=[self.slug] 
        # kwargs is a dictionary whiles args is a list
            return reverse('store:product_detail',kwargs={'slug':self.slug})

        

        

        

    