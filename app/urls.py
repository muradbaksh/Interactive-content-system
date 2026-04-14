from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.content_list, name='content_list'),
    path('create/', views.create_content, name='create_content'),
    path('content/<int:pk>/', views.content_detail, name='content_detail'),
    path('get-explanation/<int:id>/', views.get_explanation, name='get_explanation'),
    path('add-review/<int:pk>/', views.add_review, name='add_review'),
]