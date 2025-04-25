from django.urls import path
from .views import ClientSignupView, OpsSignupView, LoginView, VerifyEmailView

urlpatterns = [
    path('client-signup/', ClientSignupView.as_view()),
    path('ops-signup/', OpsSignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view()),
]