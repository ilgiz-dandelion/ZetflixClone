from django.urls import path, include

from account.views import RegistrationView, ActivateView, LoginView, LogoutView, ChangePasswordView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activation/<str:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]