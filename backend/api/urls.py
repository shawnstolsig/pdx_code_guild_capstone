from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('organizations', views.OrganizationViewSet, basename='organizations')
router.register('organizationsuuid', views.OrganizationUUIDViewSet, basename='organizationsuuid')
router.register('organizationsall', views.OrganizationAllViewset, basename="organizationall")
router.register('departments', views.DepartmentViewSet, basename='departments')
router.register('cohorts', views.CohortViewSet, basename='cohorts')
router.register('managers', views.ManagerViewSet, basename='managers')
router.register('users', views.UserViewSet, basename='users')

urlpatterns = router.urls

# for testing JWT
urlpatterns += [
    path('testAuthentication/', views.TestAuthenticationView.as_view(), name="test_authentication")
]
