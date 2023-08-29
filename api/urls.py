from django.urls import path, include
from .views import register, login, EmailBackend, get_registered_users, get_csrf_token, save_word, get_profile, get_cookie, set_cookie
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', get_profile, name='profile'),
    path('', include(router.urls)),
    path('users/', get_registered_users, name='get_registered_users'),
    path('token/', get_csrf_token, name="get-csrf-token"),
    path('save-word/<int:user_id>/', save_word, name='save-word'),

    path('get-cookie/', get_cookie, name='get-cookie'),
    path('set-cookie/<int:user_id>/', set_cookie, name='set-cookie'),

]
