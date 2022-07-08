from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from .basket import Basket
from store.models import Product
from django.http import JsonResponse
from .models import Receipt

# Create your views here.

def basket_summary(request):
    basket = Basket(request)
    return render(request,'store/store_basket/summary.html',{'basket':basket})

def basket_add(request):
    basket = Basket(request)
    receipt = Receipt()
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product,id=product_id)
        basketqty = basket.__len__()
        basket_total = basket.get_total_price()
        receipt.product_name = product.name
        receipt.item_qty = product_qty
        receipt.total_price = product_qty * product.price
        receipt.save()
        basket.add(product=product,product_qty=product_qty)
        
        response = JsonResponse({'product_qty':basketqty})
        return response 

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        basketqty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty':basketqty,'total':basket_total})
        return response

def basket_update(request):
    basket = Basket(request)
    receipt =Receipt
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id,qty=product_qty)
        Receipt.item_qty = product_qty
        # get the length of the items in the basket
        basketqty = basket.__len__()
        basket_total = basket.get_total_price()
        receipt.total_price = basket_total
        receipt.save()
        response = JsonResponse({'qty':basketqty,'total':basket_total})
        return response

