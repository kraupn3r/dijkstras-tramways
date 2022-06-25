
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from backend.api.views import SearchView
from django.views.decorators.cache import never_cache

urlpatterns = [
    # http://localhost:8000/
    path('', never_cache(TemplateView.as_view(
        template_name='index.html')), name='index'),
    path('app.js', never_cache(TemplateView.as_view(
        template_name='app.js')), name='appjs'),
]
urlpatterns += [
    path('api/v1.0/', include('backend.api.urls')),
    path('admin/', admin.site.urls),
    # path('', SearchView.as_view(), name="template"),
]
