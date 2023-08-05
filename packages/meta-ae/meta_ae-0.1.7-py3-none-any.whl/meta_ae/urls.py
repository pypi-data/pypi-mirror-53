from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import meta_ae_admin

app_name = "meta_ae"

urlpatterns = [
    path("admin/", meta_ae_admin.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
