from django.db import models
from isort import stream
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw

# Create your models here.
class Receipt(models.Model):
    product_name = models.CharField(max_length=100)
    # product_id = models.IntegerField()
    item_qty = models.IntegerField()
    total_price = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    code = models.ImageField(blank=True,upload_to='images/', default='images/default.jpg')


    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        f = open("myfile.txt", "w")
        
        f.write(self.product_name + ' \n' + str(self.item_qty) + ' \n' + 'total price:' + ' ' + str(self.total_price))
        f.close()
        with open('myfile.txt') as f:
            data = f.read()
        # qr_image = qrcode.make(self.product_name + ' ' + str(self.item_qty) + ' ' + 'total price:' + ' ' + str(self.total_price))
        qr_image = qrcode.make(data)
        qr_offset = Image.new('RGB',(500,500),'white')
        qr_offset.paste(qr_image)
        files_name = f'(self.product_name)-(self.id)qr.png'
        stream = BytesIO()
        qr_offset.save(stream,'PNG')
        self.code.save(files_name,File(stream),save = False)
        qr_offset.close()
        super().save(*args,**kwargs)
