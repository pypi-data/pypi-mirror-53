"""djangoldp project URL Configuration"""
from django.conf.urls import url
from .views import PendingResourcesViewSet
from .views import ValidatedResourcesViewSet

urlpatterns = [
    url(r'^resources/validated/', ValidatedResourcesViewSet.urls(model_prefix="resources-validated")),
    url(r'^resources/pending/', PendingResourcesViewSet.urls(model_prefix="resources-pending")),
]