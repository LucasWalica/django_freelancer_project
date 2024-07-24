from django.urls import path
from .views import (HomeView, RegisterView, LoginView, 
                        LogoutView, PasswordResetView, 
                        CustomPasswordResetConfirmView, 
                        PasswordResetCompleteView, 
                        PasswordResetDoneView)


from .views import send_test_email

#check logout 
urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('send-test-email/', send_test_email),
]