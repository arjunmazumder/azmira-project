from django.contrib import admin
from django.urls import path, include
import users.urls  # Import the specific urls module
import projects.urls
import orders.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(users.urls)), # Now this variable exists
    path('', include(projects.urls)), # Now this variable exists
    path('', include(orders.urls)), # Now this variable exists
]