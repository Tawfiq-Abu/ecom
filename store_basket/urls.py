from django.urls import path 
from . import views


app_name = 'store_basket'


urlpatterns = [
     path('',views.basket_summary,name='basket'),
     path('add/',views.basket_add,name='basket_add'),
     path('delete/',views.basket_delete,name='basket_delete'),
     path('update/',views.basket_update,name='basket_update'),
     path('qrcode/generate/',views.generate_qr_code,name='generate_qr_code'),
     path('qrcode/view/<int:pk>/', views.view_qr_code, name='view_qr_code')
]
