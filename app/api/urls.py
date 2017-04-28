from rest_framework.routers import DefaultRouter
from api.views import UserViewSet as user_view

router = DefaultRouter()
router.register(r'users', user_view)


urlpatterns = router.urls
