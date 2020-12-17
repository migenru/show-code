from django.urls import path

from q_and_a import views


app_name = 'q_and_a'
urlpatterns = [
    path('', views.index, name='index'),
    path('create-question/', views.create_question, name='create-q'),
    path('questions/', views.pre_create_answer, name='questions'),
    path('create-answer/<int:id>', views.create_answer, name='create-a'),
]
