from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from Auth.views import UserViewSet

router = DefaultRouter()
router.register(r'auth',UserViewSet,base_name='users')

urlpatterns = [
    url(r'^', include(router.urls))
]