
from django.contrib import admin
from django.urls import path, include
from student_marksheet.views import GeneratePDFView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('student_marksheet.urls')),
    path('generate-pdf/<roll>', GeneratePDFView.as_view(), name='generate_pdf'),

]
