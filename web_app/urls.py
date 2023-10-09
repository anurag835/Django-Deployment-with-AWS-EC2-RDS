
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from student_marksheet.views import GeneratePDFView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('student_marksheet.urls')),
    path('generate-pdf/<roll>', GeneratePDFView.as_view(), name='generate_pdf'),
]

# Add the following line to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)