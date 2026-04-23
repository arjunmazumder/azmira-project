from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import CreateBookingView, BookingViewSet

# Using a router for standard Admin/ERP management
router = DefaultRouter()
router.register(r'manage-bookings', BookingViewSet, basename='booking-admin')

urlpatterns = [
    # Admin & ERP Routes
    path('', include(router.urls)),

    # Customer & App Routes
    path('book-property/', CreateBookingView.as_view(), name='create-booking'),
    
    # Dashboard Tracking [cite: 55, 57]
    path('my-bookings/', BookingViewSet.as_view({'get': 'list'}), name='customer-bookings'),
]