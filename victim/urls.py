from django.conf.urls import url
from django.views.generic import TemplateView
from victim.views import VictimCreateView, VictimSearchView

urlpatterns = [
    url(r'^create$', VictimCreateView.as_view()),
    url(r'^search$', VictimSearchView.as_view()),
    url(r'^success$', TemplateView.as_view(template_name='victim/created_successfully.html'))
]