from django.urls import path

from .views import UserLoginView, UserLogoutView, classify_view, history_view, signup_view

urlpatterns = [
    path('', classify_view, name='classify'),
    path('history/', history_view, name='history'),
    path('signup/', signup_view, name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
