'''
urls.py
'''
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/signin/', views.signin, name='user/signin/'),
    path('user/signup/', views.signup, name='user/signup/'),
    path('user/logout/', views.signout, name='user/logout/'),
    path('user/token/', views.token, name='user/token/'),
    path('outfit/', views.outfit_list, name='outfit/'),
    path('outfit/<int:outfit_id>/', views.outfit, name='outfit/get_outfit/'),
    path('outfit/samplecloth/<int:samplecloth_id>/', views.sample_cloth, name='outfit/get_samplecloth/'),
    path('outfit/today/', views.today_outfit, name='outfit/today/')
]
