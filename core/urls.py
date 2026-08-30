from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


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
    path('logout/', views.custom_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-approved/', views.admin_approved_view, name='admin_approved'),
    path('admin-pending/', views.admin_pending_view, name='admin_pending'),
    path('admin-action/<int:member_id>/<str:action>/', views.admin_action_view, name='admin_action'),
    path('custom-admin-login/', views.custom_admin_login_view, name='custom_admin_login'),
    
]

