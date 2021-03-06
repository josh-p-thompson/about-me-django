from django.urls import path

import views

urlpatterns = [
    path('', views.index),
    path('projects', views.projects),
    path('blog', views.blog),
]

# Boilerplate to include static files
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

