from django.contrib import admin
from django.urls import path, include
import users.urls  # Import the specific urls module

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(users.urls)), # Now this variable exists
]