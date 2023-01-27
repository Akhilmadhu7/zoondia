from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#model for products
class Products(models.Model):
    name = models.CharField(max_length=120,unique=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='image')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

#Guestuser model for creating and store cart_id 
class GuestUser(models.Model):
    cart_id = models.CharField(max_length=130)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class Cart(models.Model):

    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,null=True,blank=True)
    guest_user = models.ForeignKey(GuestUser,related_name='guest_user',on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Products,related_name='product',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name
    


    