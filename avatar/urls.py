from django.urls import path
from . import views

app_name = 'avatar'

urlpatterns = [
    path('', views.index, name='index'),  # Homepage with the form
    path('result/<path:video_path>/', views.result, name='result'),  # Page to show the video
    path('download/<path:video_path>/', views.download_video, name='download_video'),  # Download link for the video
]