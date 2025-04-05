from django.db import models
from django.forms import ValidationError

# Create your models here.
class Admin(models.Model):
    username=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)


from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    image = models.ImageField(upload_to='category_images/', verbose_name="Category Image", null=True, blank=True)
    number = models.IntegerField(verbose_name="Category Number", null=True, blank=True)
    description = models.TextField(verbose_name="Category Description", null=True, blank=True)

    def __str__(self):
        return self.name



# models.py
class Level(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='level_icons/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='lesson_images/')
    icon = models.ImageField(upload_to='lesson_icons/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)  # Changed to ForeignKey

    def __str__(self):
        return self.name

# models.py
class Survey(models.Model):
    title = models.CharField(max_length=100, verbose_name="Survey Title")
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    text = models.TextField(verbose_name="Question Text", null=True, blank=True)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    correct_answer = models.IntegerField(verbose_name="Correct Answer")

    def clean(self):
        if self.correct_answer not in [1, 2, 3, 4]:
            raise ValidationError({'correct_answer': 'Correct answer must be 1, 2, 3, or 4.'})

    def __str__(self):
        return self.text[:50] if self.text else f"Question {self.id}"

    @property
    def level(self):
        return self.lesson.level if self.lesson else None

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_number = models.IntegerField(verbose_name="Option Number")
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='option_images/', null=True, blank=True)

    def __str__(self):
        return f"Option {self.option_number} for Question {self.question.id}"



from django.db import models
from django.utils import timezone

class SignQuiz(models.Model):
    title = models.CharField(max_length=100, verbose_name="Quiz Title")
    level = models.ForeignKey('Level', on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(default=timezone.now)
    # You might want to add more fields here, such as:
    # description, time_limit, is_published, etc.

    def __str__(self):
        return self.title

class SignQuizQuestion(models.Model):
    quiz = models.ForeignKey(SignQuiz, on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['quiz', 'question']

    def __str__(self):
        return f"Question {self.order+1} in {self.quiz.title}"


from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    def __str__(self):
        return self.question
