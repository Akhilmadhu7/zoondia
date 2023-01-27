from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from . serializers import UserSerializer,ProductSerializer,CartSerializer
from rest_framework.decorators import api_view,APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView
from . models import Products, GuestUser, Cart
from rest_framework import permissions

# Create your views here.


  


#signup function.
class Register(APIView):

    def post(self,request):
        data = {}
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            data['username'] = user.username
            token,create = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data['Response'] = 'Something went wrong' 
            data['errors'] = user_serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)   


#Add products
class AddProducts(APIView):

    parser_classes = (MultiPartParser,FormParser)

    def post(self,request):
        data = {}
        product_ser = ProductSerializer(data=request.data)
        if product_ser.is_valid():
            product_ser.save()
            data['Response'] = 'Product added succesfully'
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data['Response'] = product_ser.errors
            data['errors'] = 'Something went wrong'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)  


#List all products
class ListProducts(ListAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):
        return Products.objects.all()


#Edit products
class EditProducts(APIView):

    parser_classes = (MultiPartParser,FormParser)

    def get_object(self,id):
        try:
            return Products.objects.get(id=id)
        except:
            return None 

    def patch(self,request,id):
        print('requset is here',request.user)
        data = {}
        prod_obj = self.get_object(id)
        if prod_obj:
            prod_obj.name = request.data.get('name',prod_obj.name)
            prod_obj.price = request.data.get('price',prod_obj.price)
            prod_obj.quantity = request.data.get('quantity',prod_obj.quantity)
            prod_obj.image = request.data.get('image',prod_obj.image)
            prod_obj.status = request.data.get('status',prod_obj.status)
            prod_obj.save()
            prod_ser = ProductSerializer(prod_obj,context={'request':request})
            data['Response'] = prod_ser.data
            return Response(data, status=status.HTTP_200_OK)       
        else:
            data['Response'] = 'Product does not exist'
            return Response(data, status=status.HTTP_302_FOUND) 


class AddCart(APIView):

    #create cart id for guest users to store the cart products.
    def cart_id(self,request):                 
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart 

    #getting the user instance
    def get_user(self,id):
        try:
            return User.objects.get(id=id)
        except:
            data= {'Response':"User does not exist"} 
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 

    #getting the product instance
    def get_object(self,id):
        try:
            return Products.objects.get(id=id)
        except:
            data= {'Response':"Product does not exist"} 
            return Response(data, status=status.HTTP_400_BAD_REQUEST)       

    
    def post(self,request):
        data = {}
        prod_id = request.data['product']
        prod_obj = self.get_object(prod_id) 
        user_id = request.data['user']
        user_obj = self.get_user(user_id)

        #if the user is authenticated
        if request.user.is_authenticated:
            print('asdfkljasd',request.user.id)
            try: 
                #if the particular product is already in the user cart, then we want to increase the quantity of the cartiem quantity
                cart = Cart.objects.get(product =prod_obj, user = user_obj)
                cart.quantity += 1
                cart.save() 
                data['Response'] = 'Added'
                return Response(data,status=status.HTTP_200_OK)

            except:
                #if the product is not present in the user cart item, then we want to create the cart 
                cart = Cart.objects.create(product=prod_obj,user=user_obj,quantity = 1)
                cart.save()
                data['Response'] = 'Added'
                return Response(data, status=status.HTTP_201_CREATED)
        #guest user            
        else:
            try: 
                #if cart id(which means the guest user already added a product to cart,so we need to get the cart_id)
                guest_user = GuestUser.objects.get(cart_id=self.cart_id(request))

            except:
                 #if no cartid (first time adding a product to cart), so we want to create a new cart id
                guest_user = GuestUser.objects.create(cart_id=self.cart_id(request))  
                guest_user.save()

            try:
                    #if the particular product already in the cart of the guest user cartitems, then we need to increase the quantity + 1
                cart = Cart.objects.get(product=prod_obj,guest_user=guest_user)
                cart.quantity += 1
                cart.save()

            except:
                 # if the product is not present in the cart item, then we need to create a new cartitem with the guestuser and product
                cart = Cart.objects.create(product=prod_obj,guest_user=guest_user,quantity=1)
                cart.save()
                cart = CartSerializer(data=request.data)
                data['Response'] = 'added'
                return Response(data,status=status.HTTP_201_CREATED)
        

    def get(self,request):
        data={}
        if request.user.is_authenticated:
            user_id = request.user.id
            user_obj = self.get_user(user_id)
            try:
                cart = Cart.objects.filter(user = user_obj)
                cart_ser = CartSerializer(cart,many=True)
                data['Response'] = cart_ser.data
                return Response(data,status=status.HTTP_200_OK)
            except:
                data['Response'] = 'something went wrong'
                return Response(data,status=status.HTTP_400_BAD_REQUEST)   
        else:
            guest_user = self.cart_id(request)
            try:
                cart = Cart.objects.filter(guest_user=guest_user)
                cart_ser = CartSerializer(cart,many=True)
                data['Response'] = cart_ser.data
                return Response(data,status=status.HTTP_200_OK)
            except:
                data['Response'] = 'something went wrong'
                return Response(data,status=status.HTTP_400_BAD_REQUEST)      

                
                
                
               


