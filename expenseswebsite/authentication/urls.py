from .views import EmailValidationView, LoginView, LogoutView,RegistrationView, UserNameValidationView, VerificationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('validate-username',csrf_exempt( UserNameValidationView.as_view()),
    name="validate-username"),
    path('validate-email', csrf_exempt (EmailValidationView.as_view()),
    name='validate-email'),

    path('logout', LogoutView.as_view(), name = "logout"),
    path('login', LoginView.as_view(), name = "login"),

    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate")

]
