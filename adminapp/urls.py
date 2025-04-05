from django.urls import path
from.import views
from .views import *

urlpatterns = [
    path("", login_view, name="login"),
    path('admin_index/',views.admin_index,name='admin_index'),
    path('add_category/', views.add_category, name='add_category'),
    path('categories/', category_list, name='category_list'),
 
    path('categories/<int:pk>/edit/', category_update, name='category_update'),
    path('categories/<int:pk>/delete/', category_delete, name='category_delete'),
    path('lessons/', views.add_lesson, name='add_lesson'),
    
    path('lessons-list/', views.lesson_list, name='lesson_list'),
    path('delete-lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
    path('lesson/edit/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),
  
    path("add-question/", add_question, name="add_question"),# In your urls.py
    

   path('manage-levels/', views.manage_levels, name='manage_levels'),
    path('edit-level/<int:level_id>/', views.edit_level, name='edit_level'),  # Use a separate view for editing
    path('delete-level/<int:level_id>/', views.delete_level, name='delete_level'),


    path('get-lessons/<int:category_id>/', views.get_lessons, name='get_lessons'),

    path('surveys/', survey_list, name='survey_list'),
    path('surveys/<int:survey_id>/', survey_detail, name='survey_detail'),
    path('surveys/<int:survey_id>/delete/', survey_delete, name='survey_delete'),


      path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('select-quiz-questions/', views.select_quiz_questions, name='select_quiz_questions'),
    path('get-questions/<int:level_id>/', views.get_questions_by_level, name='get_questions_by_level'),
      path('levels/', views.view_all_levels, name='view_all_levels'),
    path('levels/<int:level_id>/', views.view_level_details, name='view_level_details'),

    path('delete-quiz/<int:quiz_id>/', delete_quiz, name='delete_quiz'),


     path("faqs/", faq_list, name="faq_list"),
    path("faqs/add/", add_faq, name="add_faq"),
    path("faqs/edit/<int:faq_id>/", edit_faq, name="edit_faq"),
    path("faqs/delete/<int:faq_id>/", delete_faq, name="delete_faq"),

]