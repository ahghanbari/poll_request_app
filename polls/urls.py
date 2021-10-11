from django.urls import path , include
from . import views


app_name = 'polls'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'), #this is def base
    path('',views.HomeView.as_view(), name='home'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact_us')
]