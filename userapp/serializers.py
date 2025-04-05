from .models import *
from rest_framework import serializers
from adminapp.models import *
from .models import Tbl_User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_User
        fields='__all__'

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tbl_User
        fields=['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_User
        fields = ['username', 'email', 'phone']


class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_User
        fields = ['username', 'email', 'phone','address','place']


from rest_framework import serializers
from adminapp.models import Category

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','name', 'image']

    def get_image(self, obj):
        if obj.image:
            return f"/media/{obj.image}"
        return None

from rest_framework import serializers
from adminapp.models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    
    image = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description',  'image']

    def get_image(self, obj):
        if obj.image:
            return f"/media/{obj.image}"
        return None



from rest_framework import serializers
# from .models import Question, Option

class OptionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['option_number', 'text', 'image']

    def get_image(self, obj):
        if obj.image:
            return f"/media/{obj.image}"
        return None

        
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    level_name = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 
            'text', 
            'image', 
            'correct_answer',
            'category_name',
            'level_name',
            'options'
        ]

    def get_image(self, obj):
        if obj.image:
            return f"/media/{obj.image}"
        return None

    def get_level_name(self, obj):
        # 1. Check direct lesson's level
        if obj.lesson and obj.lesson.level:
            return obj.lesson.level.name
        
        # 2. Check survey's level
        if obj.survey and obj.survey.level:
            return obj.survey.level.name
        
        # 3. Check other questions in survey for level
        if hasattr(obj, 'survey'):
            level = obj.survey.questions.exclude(
                lesson__level__isnull=True
            ).values_list('lesson__level__name', flat=True).first()
            
            if level:
                return level
        
        return None



# pratice session


from rest_framework import serializers
from adminapp.models import Question, Option

class OptionImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['image']

    def get_image(self, obj):
        if obj.image:
            return f"/media/{obj.image}"
        return None

class QuizOptionSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['option_number', 'text', 'images']

    def get_images(self, obj):
        if obj.image:
            return [{"image": f"/media/{obj.image}"}]
        return []

class QuizQuestionSerializer(serializers.ModelSerializer):
    options = QuizOptionSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'image', 'options','correct_answer']

    def get_image(self, obj):
        if obj.image:
            return f"/media/{obj.image}"
        return None

class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option = serializers.IntegerField(min_value=1, max_value=4)




# serializers.py
from rest_framework import serializers
from adminapp.models import Question, Option
from rest_framework import serializers
from adminapp.models import Question, Option
class LevelQuizQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'image', 'options']

    def get_options(self, obj):
        options = obj.options.all().order_by('option_number')
        return [{'id': option.id, 'text': option.text, 'image': self.get_option_image(option), 'option_number': option.option_number} for option in options]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_option_image(self, option):
        if option.image:
            return option.image.url
        return None

class QuizAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option = serializers.IntegerField()



from rest_framework import serializers
from adminapp.models import Level

class AllLevelSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Level
        fields = ['id', 'name', 'icon']

    def get_icon(self, obj):
        if obj.icon:
            return f"/media/{obj.icon.name}"
        return None



from rest_framework import serializers
from adminapp.models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
