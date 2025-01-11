from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderSearchView

urlpatterns = [
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("search/", OrderSearchView.as_view(), name="order-search"),
]
