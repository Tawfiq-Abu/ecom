

from store.models import Product
from decimal import Decimal


class Basket():


    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self,product,product_qty=1):
        '''
        adding and updating the users basket session data
        '''
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id]={'price':str(product.price),'qty':product_qty}
        self.save()

    def __iter__(self):
        '''
        collect the product_id in the session data to the query the database and return the products
        '''
        product_ids  = self.basket.keys()
        #a custom manager set in the models where it only displays items that are active
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()
        #including the product into the basket 
        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']*item['qty']
            #return the item
            yield item


    def __len__(self):
        '''
        get the basket data and count the quantity of items in it.
        '''
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self,product):
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self,product,qty):
        '''
        update values in session data
        '''
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()


    def save(self):
        self.session.modified = True
