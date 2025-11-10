from django.urls import path
from .views import SignUpView, logout
from registration import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('log-out/', views.logout, name='log-out'),
]