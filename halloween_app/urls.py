from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("studio/", views.studio, name="studio"),
    path('get-fashion-analysis/', views.get_fashion_analysis, name='get_fashion_analysis'),
    path("pre-aquecer/", views.warmup),
]