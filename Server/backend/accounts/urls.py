from django.urls import path
from . views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register',Register.as_view(),name='register'),
    path('login',obtain_auth_token,name='login'),
    path('add-product',AddProducts.as_view(),name='add-product'),
    path('list-products',ListProducts.as_view(),name='list-products'),
    path('edit-product/<int:id>',EditProducts.as_view(),name='edit-product'),
    path('add-cart',AddCart.as_view(),name='add-cart')
]
