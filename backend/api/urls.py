from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# organization routes
router.register('organizations', views.OrganizationViewSet, basename='organizations')
router.register('organizationsuuid', views.OrganizationUUIDViewSet, basename='organizationsuuid')
router.register('organizationsall', views.OrganizationAllViewSet, basename="organizationall")
router.register('departments', views.DepartmentViewSet, basename='departments')
router.register('cohorts', views.CohortViewSet, basename='cohorts')

# people routes
router.register('managers', views.ManagerViewSet, basename='managers')
router.register('workers', views.WorkerViewSet, basename='workers')
router.register('users', views.UserViewSet, basename='users')
router.register('roles', views.RoleViewSet, basename='roles')

# process routes
router.register('workspaces', views.WorkspaceViewSet, basename='workspaces')
router.register('workspacesall', views.WorkspaceAllViewSet, basename='workspacesall')
router.register('zones', views.ZoneViewSet, basename='zones')
router.register('nodes', views.NodeViewSet, basename='nodes')

# urlconf
urlpatterns = router.urls

# for testing JWT
urlpatterns += [
    path('testAuthentication/', views.TestAuthenticationView.as_view(), name="test_authentication")
]
