from django.urls import path
from core import views
from django.contrib.auth import views as auth_views

core_urlpatterns = ([    
    path('', views.home, name='home'),
    #path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    #path('about/', views.about, name='about'),
    #path('faq/', views.faq, name='faq'),
    
    #path('visit-us/', views.visit_us, name='visit-us'),   
    ], 'core')


    