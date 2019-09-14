from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('singlenews/<int:news_id>/', views.singlenews, name='singlenews'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/', views.register,name='register'),
    path('search/', views.search,name='search'),
    path('comment/', views.comment, name='comment'),
    path('pay/', views.pay, name='pay'),
    path('mv/<int:pg_id>/', views.mv, name='mv'),
]