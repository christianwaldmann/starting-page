from django.urls import path, include
from .views import RegisterView, LoginView, UserView, DeleteView
from knox import views as knox_views


urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterView.as_view()),
    path('api/auth/login', LoginView.as_view()),
    path('api/auth/user', UserView.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view()),
    path('api/auth/delete', DeleteView.as_view()),
]
