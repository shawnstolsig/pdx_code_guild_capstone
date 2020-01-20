from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('organizations', views.OrganizationViewSet, basename='organizations')
router.register('departments', views.DepartmentViewSet, basename='departments')
router.register('cohorts', views.CohortViewSet, basename='cohorts')
router.register('managers', views.ManagerViewSet, basename='managers')

urlpatterns = router.urls
