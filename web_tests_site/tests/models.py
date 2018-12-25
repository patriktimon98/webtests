from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class User_Info(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    university = models.CharField(verbose_name="Место учёбы", max_length=50, null=True, blank=True)
    specialty = models.CharField(verbose_name="Специльность", max_length=50, null=True, blank=True)
    info = models.TextField(verbose_name="Доп. информация", null=True, blank=True)

    def __str__(self):
        return str(self.user_id)

class Passed_Test(models.Model):
    test_id = models.ForeignKey('Test', on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user_id) + ' ' + str(self.test_id) + ' ' + str(self.result)

class Test(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    info = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.TextField(null=False, blank=False)
    info = models.TextField(null=True, blank=True)
    correct_answer = models.TextField(null=False, blank=False)
    test_id = models.ForeignKey('Test', on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.TextField(null=False, blank=False)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.answer