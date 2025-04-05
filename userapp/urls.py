from django.urls import path

from django.contrib import admin
from.import views
from django.urls import path, re_path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="Sign Language API",
        default_version="v1",
        description="API documentation for the sign language system.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@sign.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)

router = DefaultRouter()
router.register(r"user_registeration",UserRegistrationView,basename='user_registeration')


urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    path("",include(router.urls)),
    path('login/',LoginView.as_view(), name='login'),

    path('view_profile/<int:user_id>/', view_profile, name='view_profile'),
    path('profile/update/<int:user_id>/', update_profile, name='update_profile'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    

    path('lessons/', AllLessonsView.as_view(), name='all-lessons'),
    path('categories/<int:category_id>/lessons/', LessonByCategoryView.as_view(), name='lessons-by-category'),
    path('questions/', AllQuestionsView.as_view(), name='all-questions'),


    path('random-questions/<int:category_id>/', RandomQuestionsView.as_view(), name='random-questions'),
    path('answer-question/', AnswerQuestionView.as_view(), name='answer-question'),

 
    path('api/levels/<int:level_id>/questions/', get_level_questions),
    path('api/levels/<int:level_id>/answers/', submit_level_answers),
    
    path('levels/', LevelListView.as_view(), name='level-list'),


    path('faqs/', FAQListView.as_view(), name='faq_list_api'),
]