from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


app_name = 'backoffice'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('main/', views.main, name='main'),
    path('main/favorite', views.favorite_list, name='favorite'),
    path('profile-edit/', views.profile_edit, name='profile-edit'),
    path('logout/', LogoutView.as_view(next_page='catalog:index'), name='logout'),
    path('create-page/', views.CreatePageView.as_view(), name='create-page'),
    path('analitics/', views.analitics, name='analitics'),
    path('constructor-light/', views.constructor_light, name='constructor-light'),
]
