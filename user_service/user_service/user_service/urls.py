from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),  # login, logout, password change/reset
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # registration
    path('accounts/', include('allauth.urls')),
    path('auth/password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
