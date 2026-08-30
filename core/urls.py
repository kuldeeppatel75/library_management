from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'), # Yeh naya path add karna hai
    path('payment/', views.payment_view, name='payment_page'),
    path('login/', views.login_view, name='login_page'),
    path('setup-password/', views.setup_password_view, name='setup_password'),
    path('dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('role-select/', views.role_selection_view, name='role_selection'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('contact/', views.contact_view, name='contact_us'),
    path('contact/success', views.contact_success_view, name='contact_success'),
    
]

