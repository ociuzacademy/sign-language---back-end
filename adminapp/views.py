from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Question, Option
from django.db.models import Count

from django.views.decorators.http import require_POST



# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            admin = Admin.objects.get(username=username, password=password)
            request.session["admin_id"] = admin.id  # Store session
            return redirect("admin_index")  # Redirect to a dashboard page
        except Admin.DoesNotExist:
            return render(request, "login_view.html", {"error": "Invalid credentials"})

    return render(request, "login_view.html")

def admin_index(request):
    return render(request,'admin_index.html')

def add_category(request):
    if request.method == 'POST':
        # Get data from the request
        name = request.POST.get('name')
        image = request.FILES.get('image')  # Optional
        number = request.POST.get('number')  # Optional
        description = request.POST.get('description')  # Optional

        # Convert empty string to None for the number field
        if number == '':
            number = None

        # Create and save the category
        Category.objects.create(
            name=name,
            image=image,
            number=number,
            description=description
        )
        messages.success(request, 'Category added successfully!')  # Add success message
        return redirect('add_category')  # Redirect to the same page to show the message

    return render(request, 'add_category.html')
    

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Category

def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'category_list.html', {'categories': categories})
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        
        # Handle image update
        if 'image' in request.FILES:
            category.image = request.FILES['image']
        if request.POST.get('clear_image'):
            category.image.delete(save=False)  # Remove image
        
        # Safely handle 'number' field to avoid empty string issue
        number_value = request.POST.get('number')
        if number_value:  # If number is not an empty string
            category.number = int(number_value)
        else:
            category.number = None  # Or set a default value if required
            
        category.description = request.POST.get('description')
        category.save()
        
        messages.success(request, f'Category "{category.name}" updated successfully!')
        return redirect('category_list')
    
    return render(request, 'category_update.html', {
        'category': category
    })

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'category_confirm_delete.html', {'category': category})
    
# views.py
def add_lesson(request):
    if request.method == 'POST':
        try:
            # Basic validation
            if not all([request.POST.get('name'), 
                       request.POST.get('description'),
                       request.POST.get('category'),
                       request.FILES.get('image')]):
                raise ValueError("All required fields must be filled")

            # Get category instance
            try:
                category = Category.objects.get(name=request.POST['category'])
            except Category.DoesNotExist:
                raise ValueError("Category does not exist")

            # Get level instance if provided
            level = None
            if request.POST.get('level'):
                try:
                    level = Level.objects.get(name=request.POST['level'])
                except Level.DoesNotExist:
                    raise ValueError("Level does not exist")

            # Create lesson
            lesson = Lesson(
                name=request.POST['name'],
                description=request.POST['description'],
                category=category,
                image=request.FILES['image'],
                level=level  # Now using the Level model instance
            )

            # If icon is uploaded, save it
            if 'icon' in request.FILES:
                lesson.icon = request.FILES['icon']

            lesson.save()

            messages.success(request, 'Lesson created successfully!')
            return redirect('add_lesson')

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            categories = Category.objects.all()
            levels = Level.objects.all()
            return render(request, 'lessons.html', {
                'categories': categories,
                'levels': levels,
                'preserved_data': request.POST
            })

    # GET request
    categories = Category.objects.all()
    levels = Level.objects.all()
    return render(request, 'lessons.html', {
        'categories': categories,
        'levels': levels
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Level
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Level  # Import your Level model

def manage_levels(request):
    """Handles displaying and adding new levels"""
    levels = Level.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.FILES.get('icon')
        Level.objects.create(name=name, icon=icon)
        messages.success(request, 'Level added successfully!')
        return redirect('manage_levels')

    return render(request, 'manage_levels.html', {'levels': levels})

def edit_level(request, level_id):
    """Handles editing an existing level"""
    level = get_object_or_404(Level, id=level_id)
    
    if request.method == 'POST':
        level.name = request.POST.get('name')
        icon = request.FILES.get('icon')
        if icon:
            level.icon = icon
        level.save()
        messages.success(request, 'Level updated successfully!')
        return redirect('manage_levels')

    return render(request, 'manage_levels.html', {
        'edit_mode': True,
        'level_to_edit': level,
        'levels': Level.objects.all(),
    })


def delete_level(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    level.delete()
    messages.success(request, 'Level deleted successfully!')
    return redirect('manage_levels')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Lesson, Category, Level
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Lesson, Category, Level

def lesson_list(request):
    category_id = request.GET.get('category')
    selected_category = None

    if category_id:
        lessons = Lesson.objects.filter(category_id=category_id).select_related('category', 'level')
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        lessons = Lesson.objects.all().select_related('category', 'level')

    categories = Category.objects.all()
    return render(request, 'lesson_list.html', {
        'lessons': lessons,
        'categories': categories,
        'selected_category': selected_category,
    })

def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        try:
            lesson.delete()
            messages.success(request, 'Lesson deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting lesson: {str(e)}')
    return redirect('lesson_list')

def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if request.method == 'POST':
        try:
            # Update lesson fields
            lesson.name = request.POST.get('name')
            lesson.description = request.POST.get('description')
            lesson.category_id = request.POST.get('category')
            
            # Handle level as ForeignKey
            level_id = request.POST.get('level')
            if level_id:
                lesson.level_id = level_id
            else:
                lesson.level = None  # Clear the level if none selected

            # Handle image upload
            if 'image' in request.FILES:
                lesson.image = request.FILES['image']

            # Handle icon upload
            if 'icon' in request.FILES:
                lesson.icon = request.FILES['icon']

            lesson.save()
            messages.success(request, 'Lesson updated successfully!')
            return redirect('lesson_list')

        except Exception as e:
            messages.error(request, f'Error updating lesson: {str(e)}')
            return redirect('edit_lesson', lesson_id=lesson_id)

    # Fetch all categories and levels for the dropdowns
    categories = Category.objects.all()
    levels = Level.objects.all()
    
    return render(request, 'edit_lesson.html', {
        'lesson': lesson,
        'categories': categories,
        'levels': levels
    })

def survey_form(request): 
    # Fetch all categories to populate the dropdown
    categories = Category.objects.all()
    return render(request, 'survey_form.html', {'categories': categories})




from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Question, Option, Category

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Lesson
from django.http import JsonResponse
from .models import Lesson

def get_levels(request, id):
    """Fetch unique levels for the given category ID."""
    # Fetch unique levels and their corresponding lesson IDs
    lessons = Lesson.objects.filter(category_id=id).values('id', 'level').distinct()

    if lessons.exists():
        return JsonResponse({
            'status': 'success', 
            'levels': list(lessons)
        }, safe=False)
    else:
        return JsonResponse({
            'status': 'error', 
            'message': 'No levels found'
        }, status=404)

# views.py
def add_question(request):
    if request.method == "POST":
        try:
            survey_title = request.POST.get("survey_title")
            category_id = request.POST.get("category")
            level_id = request.POST.get("level")
            lesson_id = request.POST.get("lesson")

            # Create survey if title is provided
            survey = None
            if survey_title:
                survey, created = Survey.objects.get_or_create(
                    title=survey_title,
                    category_id=category_id if category_id else None,
                    level_id=level_id if level_id else None
                )

            # Process questions
            question_count = 1
            while f"correct_answer_{question_count}" in request.POST:
                text = request.POST.get(f"text_{question_count}", "")
                image = request.FILES.get(f"image_{question_count}")
                correct_answer = request.POST.get(f"correct_answer_{question_count}")

                # Validate correct answer
                if not correct_answer or int(correct_answer) not in [1, 2, 3, 4]:
                    messages.error(request, f"Please select a correct answer for question {question_count}")
                    return render(request, "survey_form.html", {
                        "categories": Category.objects.all(),
                        "levels": Level.objects.all()
                    })

                # Create question (text can be empty)
                question = Question.objects.create(
                    survey=survey,
                    category_id=category_id if category_id else None,
                    lesson_id=lesson_id if lesson_id else None,
                    text=text,
                    image=image,
                    correct_answer=correct_answer
                )

                # Process options
                for i in range(1, 5):
                    option_text = request.POST.get(f"option_text_{question_count}_{i}", "")
                    option_image = request.FILES.get(f"option_image_{question_count}_{i}")

                    # Only create option if either text or image is provided
                    if option_text or option_image:
                        Option.objects.create(
                            question=question,
                            option_number=i,
                            text=option_text,
                            image=option_image
                        )

                question_count += 1

            messages.success(request, "Questions added successfully!")
            return redirect("add_question")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, "survey_form.html", {
                "categories": Category.objects.all(),
                "levels": Level.objects.all()
            })

    return render(request, "survey_form.html", {
        "categories": Category.objects.all(),
        "levels": Level.objects.all()
    })

def get_lessons(request, category_id):
    try:
        lessons = Lesson.objects.filter(category_id=category_id).select_related('level')
        data = {
            'status': 'success',
            'lessons': [
                {
                    'id': lesson.id,
                    'name': lesson.name,
                    'level': lesson.level.name if lesson.level else None,
                    'level_id': lesson.level.id if lesson.level else None
                }
                for lesson in lessons
            ]
        }
    except Exception as e:
        data = {'status': 'error', 'message': str(e)}
    
    return JsonResponse(data)



def survey_list(request):
    surveys = Survey.objects.all().select_related('category')
    return render(request, 'survey_list.html', {'surveys': surveys})
from django.shortcuts import render, get_object_or_404
from .models import Survey, Question, Option
# views.py

from django.shortcuts import render, get_object_or_404
from .models import Survey, Question, Option

from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import render, get_object_or_404
from .models import Survey, Question, Option, Category, Level, Lesson

def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    
    # Get questions with related data
    questions = survey.questions.select_related(
        'category',
        'lesson',
        'lesson__level'  # Get the level through the lesson
    ).prefetch_related(
        'options'  # Prefetch options for each question
    ).order_by('id')
    
    return render(request, 'survey_detail.html', {
        'survey': survey,
        'questions': questions
    })

@require_POST
def survey_delete(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    survey.delete()
    return redirect('survey_list')










from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import SignQuiz, SignQuizQuestion, Question, Level, Survey

def create_quiz(request):
    if request.method == 'POST':
        title = request.POST.get('quiz_title')
        level_id = request.POST.get('level')
        
        if not title or not level_id:
            messages.error(request, 'Quiz title and level are required.')
            return redirect('create_quiz')
        
        # Create new quiz
        level = get_object_or_404(Level, id=level_id)
        quiz = SignQuiz.objects.create(
            title=title,
            level=level
        )
        
        # Store quiz ID in session for the question selection step
        request.session['quiz_id'] = quiz.id
        return redirect('select_quiz_questions')
    
    # GET request - show quiz creation form
    levels = Level.objects.all()
    return render(request, 'create_quiz.html', {'levels': levels})

def select_quiz_questions(request):
    quiz_id = request.session.get('quiz_id')
    if not quiz_id:
        messages.error(request, 'Quiz session expired. Please create a new quiz.')
        return redirect('create_quiz')
    
    quiz = get_object_or_404(SignQuiz, id=quiz_id)
    
    if request.method == 'POST':
        # Get selected question IDs from the form
        question_ids = request.POST.getlist('selected_questions')
        
        if not question_ids:
            messages.error(request, 'Please select at least one question.')
            return redirect('select_quiz_questions')
        
        # Clear any existing questions (in case of edit)
        SignQuizQuestion.objects.filter(quiz=quiz).delete()
        
        # Add selected questions to the quiz
        for order, question_id in enumerate(question_ids):
            SignQuizQuestion.objects.create(
                quiz=quiz, 
                question_id=question_id,
                order=order
            )
        
        # Clear the session variable
        if 'quiz_id' in request.session:
            del request.session['quiz_id']
            
        messages.success(request, f'Quiz "{quiz.title}" has been created successfully!')
        return redirect('admin_index')  # Redirect to admin dashboard or quiz list
    
    # GET request - show question selection form
    # Fetch questions for the selected level from surveys with that level
    questions = Question.objects.filter(survey__level=quiz.level).select_related('category', 'survey')
    
    return render(request, 'select_quiz_questions.html', {
        'quiz': quiz,
        'questions': questions
    })

def get_questions_by_level(request, level_id):
    """AJAX endpoint to fetch questions for a specific level"""
    try:
        # Find surveys with this level
        questions = Question.objects.filter(
            survey__level_id=level_id
        ).select_related('category', 'survey')
        
        question_list = []
        for q in questions:
            question_list.append({
                'id': q.id,
                'text': q.text[:50] + '...' if q.text and len(q.text) > 50 else (q.text or f"Question {q.id}"),
                'category': q.category.name,
                'survey': q.survey.title
            })
        
        return JsonResponse({
            'status': 'success',
            'questions': question_list
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })






# views.py
from django.shortcuts import render, get_object_or_404
from .models import Level, Survey, SignQuiz, Question, Option, SignQuizQuestion

def view_all_levels(request):
    """View listing all levels"""
    levels = Level.objects.all()
    
    # Count quizzes for each level
    for level in levels:
        # Count both types of quizzes
        level.survey_count = Survey.objects.filter(level=level).count()
        level.sign_quiz_count = SignQuiz.objects.filter(level=level).count()
        level.total_quizzes = level.survey_count + level.sign_quiz_count
    
    return render(request, 'view_all_levels.html', {
        'levels': levels
    })


from django.shortcuts import render, get_object_or_404
from .models import Level, Survey, SignQuiz, SignQuizQuestion, Question, Option
def view_level_details(request, level_id):
    """View details of a specific level with all its quizzes and questions"""
    level = get_object_or_404(Level, id=level_id)
    
    # Get all surveys (quizzes) for this level with related questions and options
    surveys = Survey.objects.filter(level=level).prefetch_related(
        'questions', 'questions__options', 'category'
    )

    # Get all sign quizzes with their questions
    sign_quizzes = SignQuiz.objects.filter(level=level).prefetch_related(
        'quiz_questions__question', 'quiz_questions__question__options'
    )
    
    # Organize survey quizzes
    organized_surveys = []
    for survey in surveys:
        questions_data = []
        for question in survey.questions.all():
            # Skip questions with no text and no image
            if not question.text and not question.image:
                continue
                
            options = list(question.options.all().order_by('option_number'))
            
            # Safely get text and image URL
            question_text = question.text or "Image Question"
            image_url = question.image.url if question.image and hasattr(question.image, 'url') else None
            
            questions_data.append({
                'id': question.id,
                'text': question_text,
                'image_url': image_url,
                'options': options,
                'correct_answer': question.correct_answer
            })
        
        # Only include surveys that have questions after filtering
        if questions_data:
            organized_surveys.append({
                'id': survey.id,
                'title': survey.title,
                'category': survey.category.name if survey.category else "Uncategorized",
                'created_at': survey.created_at,
                'questions': questions_data,
                'question_count': len(questions_data)
            })
    
    # Similar update for sign quizzes
    organized_sign_quizzes = []
    for quiz in sign_quizzes:
        questions_data = []
        for quiz_question in quiz.quiz_questions.all().order_by('order'):
            question = quiz_question.question
            
            # Skip questions with no text and no image
            if not question.text and not question.image:
                continue
                
            options = list(question.options.all().order_by('option_number'))
            
            # Safely get text and image URL
            question_text = question.text or "Image Question"
            image_url = question.image.url if question.image and hasattr(question.image, 'url') else None
            
            questions_data.append({
                'id': question.id,
                'text': question_text,
                'image_url': image_url,
                'options': options,
                'correct_answer': question.correct_answer,
                'order': quiz_question.order + 1
            })
        
        # Only include quizzes that have questions after filtering
        if questions_data:
            organized_sign_quizzes.append({
                'id': quiz.id,
                'title': quiz.title,
                'created_at': quiz.created_at,
                'questions': questions_data,
                'question_count': len(questions_data)
            })
    
    return render(request, 'view_level_details.html', {
        'level': level,
        'surveys': organized_surveys,
        'sign_quizzes': organized_sign_quizzes,
        'total_quizzes': len(organized_surveys) + len(organized_sign_quizzes)
    })



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import SignQuiz

def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(SignQuiz, id=quiz_id)
    quiz.delete()
    messages.success(request, "Quiz deleted successfully.")
    return redirect('view_all_levels')  # Redirect to a relevant page after deletion



from django.shortcuts import render, get_object_or_404, redirect
from .models import FAQ

# List all FAQs
def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, "admin_faq_list.html", {"faqs": faqs})

# Add a new FAQ
def add_faq(request):
    if request.method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        FAQ.objects.create(question=question, answer=answer)
        return redirect("faq_list")  # Redirect to FAQ list after adding
    return render(request, "admin_faq_form.html", {"action": "Add"})

# Edit an existing FAQ
def edit_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == "POST":
        faq.question = request.POST.get("question")
        faq.answer = request.POST.get("answer")
        faq.save()
        return redirect("faq_list")
    return render(request, "admin_faq_form.html", {"faq": faq, "action": "Edit"})

# Delete an FAQ
def delete_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.delete()
    return redirect("faq_list")
