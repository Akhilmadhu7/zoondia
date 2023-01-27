from rest_framework import serializers
from django.contrib.auth.models import User
from . models import Products, Cart


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs = {'password':{'write_only':True}}

    def save(self):
        user = User(username=self.validated_data['username'],
        email = self.validated_data['email'])  
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({"Password":"Password must match"})
        user.set_password(password) 
        user.save()
        return user  


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'
    status = serializers.BooleanField(default=True) 




class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = '__all__'
        depth = 1