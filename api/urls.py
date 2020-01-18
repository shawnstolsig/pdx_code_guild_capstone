from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = router.urls











''
# sample route:
# router.register('players', views.PlayerViewSet, basename='players')