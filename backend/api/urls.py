from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('organizations', views.OrganizationViewSet, basename='organizations')
router.register('departments', views.DepartmentViewSet, basename='departments')
router.register('cohorts', views.CohortViewSet, basename='cohorts')
router.register('managers', views.ManagerViewSet, basename='managers')

urlpatterns = router.urls


# all of this below added for JWT integration
urlpatterns += [
    path('token/obtain', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('hello/', views.HelloView.as_view(), name="hello")
]