from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('upload/', views.upload_view, name='upload'),
    path('create-folder/', views.create_folder_view, name='create_folder'),
    path('delete/', views.delete_view, name='delete'),
    path('download/', views.download_view, name='download'),
]