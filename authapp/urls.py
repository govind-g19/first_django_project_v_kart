from authapp import views
from django.urls import path

urlpatterns = [
    path('signup',views.signup, name='signup'),
    path('login', views.loogin, name= 'login'),
    path('logout', views.loogout, name= 'logout'),
    path('otp-verification', views.OtpVerification, name= 'otpverification'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('request-rest-email',views.RequestRestEmailView.as_view(),name='request-rest-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),

]