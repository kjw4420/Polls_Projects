from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from polls.models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class VoteSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        #질문과 답변의 조합 일치 확인
        if attrs['choice'].question.id != attrs['question'].id:
            raise serializers.ValidationError("Question과 Choice가 조합이 맞지 않습니다.")
        
        return attrs
    
    class Meta:
        model = Vote
        fields = ['id', 'question','choice', 'voter']
        validators = [
            UniqueTogetherValidator(
                queryset = Vote.objects.all(),
                fields = ['question', 'voter']
            )
        ]

class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField() #count 표시
    
    class Meta:
        model = Choice
        fields = ['choice_text','votes_count']
    
    def get_votes_count(self,obj):
        return obj.vote_set.count()
        
class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    choices = ChoiceSerializer(many = True, read_only = True)
    
    class Meta: #ModelSerializer
        model = Question
        fields = ['id','question_text', 'pub_data', 'owner','choices']



class UserSerializer(serializers.ModelSerializer):
    questions = serializers.HyperlinkedRelatedField(many = True, read_only=True, view_name='question-detail')
    # questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    # questions = serializers.StringRelatedField(many=True, read_only=True)
    # questions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pub_data')
    
    
    class Meta:
        model = User
        fields = ['id', 'username', 'questions']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True, validators= [validate_password])
    password2 = serializers.CharField(write_only =True)    
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"두 패스워드가 일치하지 않습니다."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        
        return user
        
        
    class Meta:
        model = User
        fields = ['username', 'password','password2']
        extra_kwargs = {'password':{'write_only': True}}