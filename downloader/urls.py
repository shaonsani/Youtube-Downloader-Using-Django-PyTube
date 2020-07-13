from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('download/<str:id>',views.download,name="download"),
    path('playlist/',views.playlist,name="playlistt"),
    path('playlist/download/',views.playlistDownload,name="downloads")
]