from django.contrib import admin
from django.urls import include,path
from .views import *
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('imginf/',infer.as_view(),name="imginf"),
    path('imglist/',ImgListApi.as_view()),
    path('imglist/<int:pk>/',ImgDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)