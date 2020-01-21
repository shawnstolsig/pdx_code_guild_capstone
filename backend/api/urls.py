from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('organizations', views.OrganizationViewSet, basename='organizations')
router.register('departments', views.DepartmentViewSet, basename='departments')
router.register('cohorts', views.CohortViewSet, basename='cohorts')
router.register('managers', views.ManagerViewSet, basename='managers')
router.register('users', views.UserViewSet, basename='users')

urlpatterns = router.urls


# all of this below added for JWT integration
urlpatterns += [
    path('token/obtain', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

# for testing JWT
urlpatterns += [
    path('hello/', views.HelloView.as_view(), name="hello")
]