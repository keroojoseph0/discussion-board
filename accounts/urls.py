from django.urls import path
from . import views 
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('signup', views.signup, name = 'signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', views.CustomUserLogin.as_view(), name = 'login'),
    path('reset/', views.CustomUserPasswordReset.as_view(), name = 'reset'),
]
