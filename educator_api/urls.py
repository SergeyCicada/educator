from django.urls import path
from .views import EmployeeList, EmployeeDetail
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("<int:pk>/", EmployeeDetail.as_view(), name="employee_detail"),
    path("", EmployeeList.as_view(), name="employee_list"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
