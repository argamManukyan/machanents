from django.urls import path
from .views import (ActivationEmail, ForgotPassword, 
                    LoginView, RegisterView, ProfileView, 
                    NewPasswordView, logout_view,ChangePasswordView,
                    OrderDetails)

urlpatterns = [

    path('sign-up/',RegisterView.as_view(),name='register'),
    path('sign-in/',LoginView.as_view(),name='login'),
    path('logout/',logout_view,name='logout'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    path('me/',ProfileView.as_view(),name='profile'),
    path('forgot-password/',ForgotPassword.as_view(),name='forgot'),
    path('password-reset-confirm/<uid64>/<token>/',NewPasswordView.as_view(),name='password_reset_confirm'),
    path('activation/<uid64>/<token>/',ActivationEmail.as_view(),name='activation'),
    path('order-details/<pk>/',OrderDetails.as_view(),name='user_order'),

]
