from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status,viewsets,generics
from rest_framework.views import APIView
from adminapp.models import *
import random


# Create your views here.


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = Tbl_User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "User created successfully",
                "data": serializer.data  # This will show the saved user data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors,  # Optionally show validation errors
                "data": request.data  # This will show the data that was sent
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')

            try:
                user = Tbl_User.objects.get(email=email)

                if password == user.password:  # Directly comparing (consider Django's authentication)
                    request.session['id'] = user.id  # Save user ID in session
                    return Response({
                        "status": "success",
                        "message": "User logged in successfully",
                        "user_id": str(user.id),
                        "user_email":user.email,
                        "user_password":user.password,
                        "user_name":user.username
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except Tbl_User.DoesNotExist:
                return Response({"status": "failed", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "failed", "message": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view
@api_view(['GET'])
def view_profile(request, user_id):
    try:
        user = Tbl_User.objects.get(id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    except Tbl_User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)




from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Tbl_User
from .serializers import UserEditProfileSerializer

@api_view(['PATCH'])  # Use PATCH for partial updates instead of PUT
def update_profile(request, user_id):
    try:
        user = Tbl_User.objects.get(id=user_id)
    except Tbl_User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserEditProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import ListAPIView
from adminapp.models import Category
from .serializers import CategorySerializer

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


from rest_framework.generics import ListAPIView
from adminapp.models import Lesson
from .serializers import LessonSerializer


from rest_framework.generics import ListAPIView


class AllLessonsView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.select_related('category').all()

class LessonByCategoryView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Lesson.objects.filter(category_id=category_id).select_related('category')





from rest_framework.generics import ListAPIView
from adminapp.models import Question
from .serializers import QuestionSerializer


class AllQuestionsView(ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.select_related(
        'category',
        'lesson__level',
        'survey',
        'survey__level'
    ).prefetch_related(
        'options'
    ).all()



# pratice session


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import random
from adminapp.models import Question, Option
from .serializers import QuizQuestionSerializer, AnswerSerializer

class RandomQuestionsView(APIView):
    def get(self, request, category_id):
        questions = Question.objects.filter(
            category_id=category_id
        ).prefetch_related('options')
        
        if not questions.exists():
            return Response(
                {"error": "No questions found for this category"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get 5 random questions
        random_questions = random.sample(list(questions), min(len(questions), 5))
        serializer = QuizQuestionSerializer(random_questions, many=True)
        return Response(serializer.data)

class AnswerQuestionView(APIView):
    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        question = get_object_or_404(Question, id=data['question_id'])
        selected_option = question.options.filter(
            option_number=data['selected_option']
        ).first()
        correct_option = question.options.filter(
            option_number=question.correct_answer
        ).first()
        
        # Serialize the options
        selected_serializer = QuizOptionSerializer(selected_option)
        correct_serializer = QuizOptionSerializer(correct_option)
        
        if data['selected_option'] == question.correct_answer:
            return Response({
                "message": "Correct Answer!"
            })
        else:
            return Response({
                "message": "Incorrect Answer!",
                "your_answer": selected_serializer.data,
                "correct_answer": correct_serializer.data
            }, status=status.HTTP_200_OK)







from rest_framework.permissions import IsAuthenticated
import random
from rest_framework import serializers, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone


from rest_framework.permissions import IsAuthenticated
import random
from rest_framework import serializers, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import serializers, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
# from .models import Tbl_User, Level, UserLevelProgress, SignQuiz, SignQuizQuestion, Question, Option, UserAnswer




# views.py
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from .models import Question, Option, SignQuizQuestion, Tbl_User

@api_view(['GET'])
def get_level_questions(request, level_id):
    user_id = request.query_params.get('user_id')

    if not user_id:
        return Response(
            {"error": "user_id parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Verify if user exists
        Tbl_User.objects.get(id=user_id)

        # Get questions linked through Lessons
        lesson_questions = Question.objects.filter(
            lesson__level_id=level_id
        ).values_list('id', flat=True)

        # Get questions linked through Quizzes
        quiz_questions = SignQuizQuestion.objects.filter(
            quiz__level_id=level_id
        ).values_list('question_id', flat=True)

        # Combine both sets of questions
        question_ids = list(set(lesson_questions) | set(quiz_questions))
        
        if not question_ids:
            return Response({
                "questions": [],
                "level_id": level_id,
                "message": "No questions available for this level"
            })

        # Retrieve questions and serialize them
        questions = Question.objects.filter(id__in=question_ids).order_by('?')[:5]
        
        serialized_questions = []
        for question in questions:
            options = Option.objects.filter(question=question).order_by('option_number')
            serialized_questions.append({
                "id": question.id,
                "text": question.text,
                "image": question.image.url if question.image else None,
                "correct_answer": question.correct_answer,
                "options": [
                    {
                        "id": opt.id,
                        "text": opt.text,
                        "image": opt.image.url if opt.image else None,
                        "option_number": opt.option_number
                    } for opt in options
                ]
            })

        return Response({
            "questions": serialized_questions,
            "level_id": level_id,
            "total_questions": len(serialized_questions)
        })

    except Tbl_User.DoesNotExist:
        return Response(
            {"error": "Invalid user_id"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
from django.db.models import Sum


@api_view(['POST'])
def submit_level_answers(request, level_id):
    user_id = request.data.get('user_id')
    answers = request.data.get('answers', [])
    
    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = Tbl_User.objects.get(id=user_id)
        level = Level.objects.get(id=level_id)
    except Tbl_User.DoesNotExist:
        return Response(
            {"error": "Invalid user_id"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Level.DoesNotExist:
        return Response(
            {"error": "Level not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Process answers and calculate score
    score = 0
    for answer in answers:
        try:
            question = Question.objects.get(id=answer['question_id'])
            if question.correct_answer == answer['selected_option']:
                score += 10
            UserAnswer.objects.create(
                user=user,
                question=question,
                selected_option=answer['selected_option']
            )
        except Question.DoesNotExist:
            continue
    
    # Update user progress
    progress, created = UserLevelProgress.objects.get_or_create(
        user=user,
        level=level,
        defaults={'score': score, 'completed': score >= 30}
    )
    
    if not created:
        if progress.completed:
            total_score = UserLevelProgress.objects.filter(
                user=user, completed=True
            ).aggregate(total=Sum('score'))['total'] or 0
            
            return Response({
                "status": "already_completed",
                "score": progress.score,
                "total_score": total_score,
                "message": "Level already completed."
            })
        
        progress.score = score
        progress.completed = score >= 30
        progress.save()
    
    # Calculate total score (Fix applied)
    total_score = UserLevelProgress.objects.filter(
        user=user, 
        completed=True
    ).aggregate(total=Sum('score'))['total'] or 0  # Ensures it is never None
    
    if progress.completed:
        next_level = Level.objects.filter(id__gt=level_id).order_by('id').first()
        
        response_data = {
            "status": "passed",
            "score": score,
            "total_score": total_score,
            "message": "Level passed! Proceeding to next level."
        }
        
        if next_level:
            response_data["next_level_id"] = next_level.id
        
        return Response(response_data)
    else:
        return Response({
            "status": "failed",
            "score": score,
            "total_score": total_score,  # Fix applied
            "message": "Level failed. Try again."
        })
from rest_framework import generics
from adminapp.models import Level
from .serializers import AllLevelSerializer

class LevelListView(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = AllLevelSerializer




from rest_framework.generics import ListAPIView
from adminapp.models import FAQ
from .serializers import FAQSerializer

class FAQListView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
