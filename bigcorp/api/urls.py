from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from . import views

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="BigCorp API",
        default_version='v1',
        description="API for BigCorp",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="oYp2V@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    # Products
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    # Reviews
    path('reviews/', views.ReviewCreateAPIView.as_view()),
    # Users
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
