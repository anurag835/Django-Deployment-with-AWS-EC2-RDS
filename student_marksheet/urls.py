from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_roll, name='input_roll'),
    path('parse-excel/', views.file_upload, name='data'),
    path('parse-excel-file/', views.simple_file_upload, name='user'),
    path('get-data/<uuid:token>', views.get_data, name='user_data'),
]
