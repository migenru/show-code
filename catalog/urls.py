from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)

app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.CategoryListView.as_view(), name='catalog'),
    path('catalog/all/', views.products_all, name='products_all'),
    path('catalog/<slug:slug>/', views.ProductListView.as_view(), ),
    path('catalog/product/<slug:slug>/', views.product_card, name='product_detail'),
    path('search/', views.get_product, name="search"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
