"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from board import views
from accounts import views as view_accounts
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('reset/done', view_accounts.CustomUserPasswordResetDone.as_view(), name = 'password_reset_done'),
    path('reset/reset/<uidb64>/<token>/', view_accounts.CustomUserPasswordResetConfirm.as_view(), name = "password_reset_confirm"),
    path('reset/complete', view_accounts.CustomUserPasswordResetComplete.as_view(), name = 'password_reset_complete'),
    path('password/change', view_accounts.CustomUserPasswordChange.as_view(), name = 'password_change'),
    path('password/done', view_accounts.CustomUserPasswordChangeDone.as_view(), name = 'password_change_done'),
    
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('boards/', include('board.urls', namespace='board_topics')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)