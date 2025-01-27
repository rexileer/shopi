from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recommend.models import Review
from shop.models import Product, Category

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', many=False, queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'brand',
            'price',
            'category',
            'image',
            'description',
            'created_at',
            'updated_at',
        ]
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'rating',
            'content',
            'created_by',
            'created_at',
            'product_id',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']
        

class ProductDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', many=False, queryset=Category.objects.all())
    discounted_price = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'brand',
            'category',
            'price',
            'discounted_price',
            'discount',
            'image',
            'available',
            'description',
            'created_at',
            'updated_at',
            'reviews',
        ]
        
    def get_discounted_price(self, obj):
        return obj.get_discounted_price()
    

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        user = User(email=email, username=username)
        user.set_password(validated_data['password'])
        user.save()
        return user