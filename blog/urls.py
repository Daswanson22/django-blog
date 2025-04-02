from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('blog/<int:pk>/', views.post_detail, name='post_detail'),
    path('upvote/<int:pk>', views.upvote, name='upvote')
]