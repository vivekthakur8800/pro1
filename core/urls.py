from django.contrib import admin
from django.urls import path,include
from core import views
from django.conf import settings
from django.conf.urls.static import static
app_name="core"
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('student',views.StudentList.as_view(),name='student'),
    path('student/<int:pk>',views.StudentDetail.as_view(),name='student_detail'),
    # path('',views.HomeView.as_view(),name='home'),
]