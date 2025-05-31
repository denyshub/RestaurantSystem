from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),  # login, logout, password change/reset
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # registration
    path('accounts/', include('allauth.urls')),
]
