from django.conf.urls import include, url
from django.contrib import admin
from matcher import views as matcher_views
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework.authtoken import views

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'keys', matcher_views.KeyViewSet)
router.register(r'tracks', matcher_views.TrackViewSet)
router.register(r'boxes', matcher_views.BoxViewSet)
# router.register(r'import', matcher_views.FileUploadView, base_name='csv')

box_tracks_router = routers.NestedSimpleRouter(
    router, r'boxes', lookup='boxes'
)
box_tracks_router.register(
    r'tracks', matcher_views.BoxTrackViewSet, base_name='box-tracks'
)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^', include(box_tracks_router.urls)),
    url(r'^get-auth-token/', views.obtain_auth_token),
    url(r'^import/', matcher_views.FileUploadView.as_view()),
]
