import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    ## __str__() 메소드를 이용해서 객체의 표현을 대화식 프롬포트에서 편하게 보고,
    ## Django가 자동으로 생성하는 관리 사이트 에서도 객체의 표현을 사용하기 위함
    def __str__(self):
        return self.question_text
    # 커스텀 메소드 추가
    # 어제 이후 발행된 데이터 반환

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    # 외래키 -> Question 데이터 모델 참조한다.
    # CASCADE -> 참조되는 모델(Question) 삭제되면 참조하는 모델(Choice)도 같이 삭제
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text