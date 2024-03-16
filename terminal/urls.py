from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "terminal"   

router = DefaultRouter()
router.register(r'users', views.UserViewSet,basename="user")



urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("sign-in", views.SignInView.as_view(), name="sign_in"),
    path("sign-up", views.SignUpView.as_view(), name="sign_up"),
    path("logout", views.logout_view, name="logout"),

    path('api/', include(router.urls)),

    re_path(r'^(?P<path>.+)/$', views.IndexView.as_view(), name="index_with_path"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)