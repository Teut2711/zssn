from django.urls import include, path
from rest_framework import routers
from survivors import views

router = routers.DefaultRouter()
router.register(r"survivors", views.SurvivorViewSet)
router.register(r"reports", views.GenerateReportViewSet, basename="report")
router.register(r"trades", views.TradeViewSet, basename="trade")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
]
