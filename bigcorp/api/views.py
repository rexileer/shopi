from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from recommend.models import Review

from shop.models import Product
from .serializers import ProductSerializer, ProductDetailSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly
from .pagination import StandardResultsSetPagination


class ProductListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').order_by('id')
    
    
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'
    
    
class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        existing_review = Review.objects.filter(created_by=self.request.user, product=product).exists()
        
        if existing_review:
            raise ValidationError("You have already reviewed this product.")
        
        serializer.save(created_by=self.request.user, product=product)