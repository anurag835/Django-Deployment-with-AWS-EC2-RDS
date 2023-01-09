from django.urls import path
from . import views

urlpatterns = [
    path('parse-excel/', views.file_upload, name='data'),
    path('parse-excel-file/', views.simple_file_upload, name='user'),
    path('get-data/<roll>', views.get_data, name='user_data'),
    path('', views.input_roll, name='input_roll'),
]
