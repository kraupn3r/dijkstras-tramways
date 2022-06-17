
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from backend.api.views import SearchView



urlpatterns = [
    path('api/v1.0/', include('backend.api.urls')),
    path('admin/', admin.site.urls),
    path('', SearchView.as_view(), name="template"),
]
