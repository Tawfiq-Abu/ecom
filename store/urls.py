from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('item/<slug:slug>/',views.StoreDetail.as_view(),name='product_detail')
]
