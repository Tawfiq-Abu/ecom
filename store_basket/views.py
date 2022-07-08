from multiprocessing import context
from random import random
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .basket import Basket
from store.models import Product
from django.http import JsonResponse
from .models import Receipt, QrCode

import qrcode
import random
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

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
    receipt =Receipt()
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id,qty=product_qty)
        receipt.item_qty = product_qty
        # get the length of the items in the basket
        basketqty = basket.__len__()
        basket_total = basket.get_total_price()
        receipt.total_price = basket_total
        receipt.save()
        response = JsonResponse({'qty':basketqty,'total':basket_total})
        return response

def view_qr_code(request, pk):
    qr_code = QrCode.objects.get(pk=pk)
    return render(request,'store/store_basket/qr_code.html', context={"qr_code": qr_code})

def generate_qr_code(request):
    basket = Basket(request)
    receipt_no = random.randrange(3000000, 9999999)
    order_summary = (
        f"Receipt No. {receipt_no}\n\n" + 
        f'{"Product Name":<25}{"Unit Price":<15}{"Quantity":<13}{"Total":<10}\n' + 
        f'{"-------------":<25}{"----------":<15}{"----------":<13}{"------":<10}\n' 
    )
    
    for product in basket:
        product_summary = f"{product['product'].name:<25}{product['price']:<15}{product['qty']:<13}{product['total_price']:<10}\n"        
        order_summary += product_summary
    print(order_summary)
    
    qr_image = qrcode.make(order_summary)
    qr_offset = Image.new('RGB',(1000,1000),'white')
    qr_offset.paste(qr_image)
    files_name = f'Receipt-{receipt_no}-qr.png'
    stream = BytesIO()
    qr_offset.save(stream,'PNG')
    qr_code = QrCode()
    qr_code.file.save(files_name, File(stream), save=False)
    qr_offset.close()
    qr_code.save()
    return redirect("store_basket:view_qr_code", pk=qr_code.pk)

    # f = open("myfile.txt", "w")
    
    # f.write(self.product_name + ' \n' + str(self.item_qty) + ' \n' + 'total price:' + ' ' + str(self.total_price))
    # f.close()
    # with open('myfile.txt') as f:
    #     data = f.read()
    # # qr_image = qrcode.make(self.product_name + ' ' + str(self.item_qty) + ' ' + 'total price:' + ' ' + str(self.total_price))
    # qr_image = qrcode.make(data)
    # qr_offset = Image.new('RGB',(500,500),'white')
    # qr_offset.paste(qr_image)
    # files_name = f'(self.product_name)-(self.id)qr.png'
    # stream = BytesIO()
    # qr_offset.save(stream,'PNG')
    # self.code.save(files_name,File(stream),save = False)
    # qr_offset.close()    
