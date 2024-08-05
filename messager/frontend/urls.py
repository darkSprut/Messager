from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'frontend'

urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/base.html"), name='index'),
]
