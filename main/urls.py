from django.urls import path

from . import studio, views


app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/login/', studio.studio_login, name='studio_login'),
    path('admin/logout/', studio.studio_logout, name='studio_logout'),
    path('admin/', studio.studio_dashboard, name='studio_dashboard'),
    path('admin/<slug:model_key>/', studio.studio_model_list, name='studio_model_list'),
    path('admin/<slug:model_key>/new/', studio.studio_model_create, name='studio_model_create'),
    path('admin/<slug:model_key>/<int:pk>/', studio.studio_model_edit, name='studio_model_edit'),
    path('admin/<slug:model_key>/<int:pk>/delete/', studio.studio_model_delete, name='studio_model_delete'),
    path('studio/', studio.studio_redirect, name='studio_redirect'),
    path('studio/<path:path>/', studio.studio_redirect, name='studio_redirect_path'),
    path('world/<slug:slug>/', views.world_detail, name='world_detail'),
    path('world/<slug:world_slug>/lesson/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('world/<slug:world_slug>/quest/<slug:quest_slug>/', views.quest_detail, name='quest_detail'),
    path('progress/', views.progress_view, name='progress'),
    path('progress/reset/', views.reset_progress, name='reset_progress'),
    path('career/', views.career_view, name='career'),
    path('textbooks/', views.textbooks_view, name='textbooks'),
    path('textbooks/<slug:book_slug>/', views.textbook_detail, name='textbook_detail'),
    path('textbooks/<slug:book_slug>/<slug:topic_slug>/', views.textbook_topic_detail, name='textbook_topic_detail'),
]
