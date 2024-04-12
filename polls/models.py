from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length = 200, verbose_name = "질문")
    pub_data = models.DateTimeField(auto_now_add= True, verbose_name = "생성일")
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null =True)
    
    @admin.display(boolean = True, description = "최근생성(하루기준)")
    def was_published_recently(self):
        return self.pub_data >= timezone.now()- datetime.timedelta(days=1)
    def __str__(self):
        if self.was_published_recently():
            new_badge = 'NEW!!!'
        else:
            new_badge = ''
            
        return f'{new_badge}제목:{self.question_text}, 날짜: {self.pub_data}'
    
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)
    
    def __str__(self):
        return f'[{self.question.question_text}]{self.choice_text}'
    
    
class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete = models.CASCADE)
    voter = models.ForeignKey(User, on_delete = models.CASCADE)
    
    #하나의 질문에 User가 한번 투표할 수 있도록(ex. 1번 질문에 1번유저 1번만 투표가능)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question','voter'], name = 'unique_voter_for_questions')
        ]