

from django.contrib import admin
from polls.views import SignUpView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/',SignUpView.as_view() , name="signup"),
    path('', include('polls.urls')),
]
