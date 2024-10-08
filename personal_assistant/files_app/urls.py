from django.urls import path
from files_app import views
from files_app.views import FileListView

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', FileListView.as_view(), name='file_list'),
]
