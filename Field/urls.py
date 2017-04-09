from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from Field.views import FieldViewSet

router = DefaultRouter()
router.register(r'fields',FieldViewSet,base_name='fields')

urlpatterns = [
    url(r'^', include(router.urls))
]