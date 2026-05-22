from django.urls import path

from . import views


urlpatterns = [
    path('', views.exercise_list, name='exercise_list'),
    path('courses/<slug:course_slug>/', views.exercise_list, name='course_detail'),
    path('progress/', views.progress_view, name='progress'),
    path('tasks/<slug:slug>/', views.exercise_detail, name='exercise_detail'),
]
