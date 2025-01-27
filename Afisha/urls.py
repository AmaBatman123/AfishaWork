"""
URL configuration for Afisha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from movie_app.views import (DirectorsListView, DirectorDetailView,
                            MoviesListView, MovieDetailView,
                            ReviewsListView, ReviewDetailView,
                            RegisterView, LoginView, ConfirmUserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', DirectorsListView.as_view(), name='directors_list'),
    path('api/v1/directors/<int:id>/', DirectorDetailView.as_view(), name='director_detail'),
    path('api/v1/movies/', MoviesListView.as_view(), name='movies_list'),
    path('api/v1/movies/<int:id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('api/v1/reviews/', ReviewsListView.as_view(), name='reviews_list'),
    path('api/v1/reviews/<int:id>/', ReviewDetailView.as_view(), name='review_detail'),
    path('api/v1/users/register/', RegisterView.as_view(), name='register'),
    path('api/v1/users/login/', LoginView.as_view(), name='login'),
    path('api/v1/users/confirm/', ConfirmUserView.as_view(), name='confirm_user'),
]
