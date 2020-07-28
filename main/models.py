from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os



# Create your models here.
class PlatformUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(default="default", max_length=40)
    job = models.CharField(default="default", max_length=40)
    activated = models.BooleanField(default=False)
    quizMaxScore = models.IntegerField(default=0)
    unlockedTalks = models.CharField(default="0", max_length=40)
    goal = models.TextField(default="None")
    submitedGoal = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    talk1UpTo = models.IntegerField(default=0)
    talk1PlayTimes = models.IntegerField(default=0)
    talk2UpTo = models.IntegerField(default=0)
    talk2PlayTimes = models.IntegerField(default=0)
    talk3UpTo = models.IntegerField(default=0)
    talk3PlayTimes = models.IntegerField(default=0)
    talk4UpTo = models.IntegerField(default=0)
    talk4PlayTimes = models.IntegerField(default=0)
    talk5UpTo = models.IntegerField(default=0)
    talk5PlayTimes = models.IntegerField(default=0)
    talk6UpTo = models.IntegerField(default=0)
    talk6PlayTimes = models.IntegerField(default=0)
    hasLoggedInAtLeastOne = models.BooleanField(default=False)
    timeBeingOnWebsite = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class SpeakersSection(models.Model):
    name = models.CharField(default="", max_length=40)
    img = models.ImageField()
    description = models.TextField()

class Talks(models.Model):
    name = models.CharField(default="", max_length=40)
    img = models.ImageField()
    lockedImg = models.ImageField()
    header = models.TextField()
    subheader = models.TextField()

class Trends(models.Model):
    name = models.CharField(default="", max_length=40)
    cover = models.ImageField(upload_to = "media")
    description = models.TextField()
    header = models.TextField(null=True, blank=True)
    info1 = models.TextField()
    info2 = models.TextField()
    mainVideo = models.TextField()
    video1 = models.TextField()
    video2 = models.TextField()
    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.TextField()
    answer1 = models.TextField()
    answer2 = models.TextField()
    answer3 = models.TextField()
    correctAnswer = models.IntegerField()
    def __str__(self):
        return self.question

class WhatsNext(models.Model):
    platformUser = models.ForeignKey(PlatformUser, on_delete=models.CASCADE)
    whatsNext = models.TextField()

class Estadisticas(models.Model):
    id = models.TextField(default="0", unique=True, primary_key=True)
    usuariosConectados = models.IntegerField(default=0)
    usuariosRegistradosQueSeLogearon = models.IntegerField(default=0)

    talk1TotalReproductions = models.IntegerField(default=0)
    talk2TotalReproductions = models.IntegerField(default=0)
    talk3TotalReproductions = models.IntegerField(default=0)
    talk4TotalReproductions = models.IntegerField(default=0)
    talk5TotalReproductions = models.IntegerField(default=0)
    talk6TotalReproductions = models.IntegerField(default=0)

    callToAction = models.IntegerField(default=0)

    rebote = models.IntegerField(default=0)
    visitasTotales = models.IntegerField(default=0)
    visitasOtherPages = models.IntegerField(default=0)

    quizTotalesAmount = models.IntegerField(default=0)
    quizCalificationAcumulative = models.IntegerField(default=0)
    timeInPage = models.IntegerField(default=0)