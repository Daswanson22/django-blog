from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('user/<slug:user_slug>', views.profile_view, name='user'),
    path('blog/<slug:blog_slug>', views.post_detail, name='post_detail'),
    path('upvote/<int:pk>', views.upvote, name='upvote'),
    path('comment/<int:pk>', views.comment, name='comment'),
    path('team/<slug:team_slug>', views.team_view, name='team'),
]