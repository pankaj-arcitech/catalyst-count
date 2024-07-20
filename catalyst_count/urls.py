"""
URL configuration for catalyst_count project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

from account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls') ),

    path("users/", views.users , name='users'),
    path("users/delete/<int:user_id>/", views.deleteUser , name='deleteUser'),
    path('upload/', views.upload_data, name='upload_data'),
    path('query/', views.query_builder, name='query_builder'),

    path('api/query/', views.QueryBuilderAPIView.as_view(), name='query-builder-api'),
]
