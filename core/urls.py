from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'), # Yeh naya path add karna hai
    path('payment/', views.payment_view, name='payment_page'),
]
