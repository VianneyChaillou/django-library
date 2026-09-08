from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import home_view
urlpatterns = [
    path('', login_required(home_view), name='home'),
]