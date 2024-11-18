from django.contrib import admin
from django.urls import path
from banani_clicker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('user', views.user, name='user'),
    path('about', views.about, name='about'),
    path('play', views.play, name='play'),
    path('how_to', views.how_to, name='how_to'),
]
