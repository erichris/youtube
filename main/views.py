# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .models import PlatformUser, Trends, Question, Estadisticas
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.http import Http404
from datetime import datetime

class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm

def validate_username(request):
    username = request.POST.get('username', None)
    data = {
        'is_taken': True
    }
    return JsonResponse(data)

def service_login(request):
    username = request.POST.get('username', None)
    data = {
        'is_taken': True
    }
    return JsonResponse(data)

def service_register(request):
    username = request.POST.get('username', None)
    data = {
        'is_taken': True
    }
    return JsonResponse(data)

@csrf_exempt
def service_contact(request):
    nombre = request.POST.get('name', None)
    correo = request.POST.get('mail', None)
    text = request.POST.get('message', None)
    subject = 'Form Contact'
    message = "Nombre: " + nombre + "<br>"
    message += "Email: " + correo + "<br>"
    message += "Message: " + text + "<br>"
    email_from = settings.EMAIL_HOST_USER

    recipient_list = [settings.EMAIL_HOST_USER, ]
    send_mail(subject, message, email_from, recipient_list, html_message=message)

    data = {
        'message': "Tu mensaje se envio exitosamente",
    }
    return JsonResponse(data)

@csrf_exempt
# Create your views here.
def Home(request):
    if request.user.is_authenticated == True:
        #raise Http404()
        return redirect('/Dashboard/')
    if request.POST:
        if request.POST['Action'] == "Register":
            username = request.POST['user']
            password = request.POST['pass']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                platformUser = PlatformUser.objects.filter(user=user).first()
                if platformUser.name == "default":
                    estadisticas = Estadisticas.objects.get(id=0)
                    estadisticas.usuariosRegistradosQueSeLogearon += 1
                    estadisticas.save()
                    if platformUser.hasLoggedInAtLeastOne == False:
                        platformUser.hasLoggedInAtLeastOne = True
                        estadisticas.usuariosConectados += 1
                    platformUser.name = request.POST['name']
                    platformUser.job = request.POST['job']
                    platformUser.unlockedTalks = "0"
                    u = User.objects.get(username=username)
                    u.set_password(request.POST['newPass'])
                    u.save()
                    platformUser.save()
                    user = authenticate(request, username=username, password=request.POST['newPass'])
                    login(request, user)
                    SendOnRegisterMail(request, platformUser.user.username)
                    return JsonResponse({
                        'content': {
                            'status': 0,
                            'redirectURL': '/Dashboard/',
                            'message': "Access Granted",
                        }
                    })
                else:
                    return JsonResponse({
                        'content': {
                            'message': "El usuario ingresado ya esta registrado",
                        }
                    })
            else:
                return JsonResponse({
                    'content': {
                        'message': "El usuario ingresado no existe",
                    }
                })
        if request.POST['Action'] == "Login":
            username = request.POST['user']
            password = request.POST['pass']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                platformUser = PlatformUser.objects.filter(user=user).first()
                if platformUser.name != "default":
                    estadisticas = Estadisticas.objects.get(id=0)
                    estadisticas.usuariosConectados += 1
                    estadisticas.save()

                    login(request, user)
                    return JsonResponse({
                        'content': {
                            'status' : 0,
                            'redirectURL': '/Dashboard/',
                            'message': "Access Granted",
                        }
                    })
                else:
                    return JsonResponse({
                        'content': {
                            'message': "Parece que es tu primera vez, aun no tienes acceso",
                        }
                    })
            else:
                return JsonResponse({
                    'content': {
                        'message': "Usuario o contraseña incorrecta",
                    }
                })
        if request.POST['Action'] == "Contact":
            subject = 'Form Contact'
            message = "Nombre: " + request.POST['nameContact'] + "<br>"
            message += "Email: " + request.POST['emailContact'] + "<br>"
            message += "Message: " + request.POST['messageContact'] + "<br>"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER, ]
            send_mail(subject, message, email_from, recipient_list, html_message=message)
            return JsonResponse({
                'content': {
                    'message': "Tu mensaje se envio exitosamente",
                }
            })
    estadisticas = Estadisticas.objects.get(id=0)
    estadisticas.visitasTotales += 1
    estadisticas.save()
    return render(request, "home.html");

def updateCont(request):
    return JsonResponse({
        'content': {
            'message': "Hola",
        }
    })

def TrendInformation(request):
    return HttpResponse("Hola mundo");



def Workshop(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    return TemplateResponse(request, "workshop.html")

def Profile(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    args = {}
    platformUser = PlatformUser.objects.get(user=request.user)
    args['User'] = request.user
    args['platformUser'] = platformUser
    return TemplateResponse(request, "Profile.html", args)

def QA(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    return TemplateResponse(request, "qa.html")

def Goals(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    return TemplateResponse(request, "Goals.html")

def CommonQuestions(request):
    return HttpResponse("Hola mundo");

def Mailing(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['erichris@live.com.mx',]
    send_mail(subject, message, email_from, recipient_list)
    return render(request, "home.html")

def Dashboard(request):
    estadisticas = Estadisticas.objects.get(id=0)
    estadisticas.visitasOtherPages += 1
    estadisticas.save()
    if request.user.is_authenticated == False:
        return redirect('/')

    args = {}
    args['trends'] = Trends.objects.all()
    platformUser = PlatformUser.objects.get(user=request.user)
    args['platformUser'] = platformUser
    args['questions'] = Question.objects.all()
    return TemplateResponse(request, "Dashboard.html", args)

def Trend(request, name):
    if request.user.is_authenticated == False:
        return redirect('/')

    args = {}
    args['trend'] = Trends.objects.get(name=name)
    return TemplateResponse(request, "SelectedTrend.html", args)

def Quiz(request):
    if request.user.is_authenticated == False:
        return redirect('/')

    args = {}
    args['questions'] = Question.objects.all()

    platformUser = PlatformUser.objects.get(user=request.user)
    args['platformUser'] = platformUser

    return TemplateResponse(request, "Quiz.html", args)


def Test(request):
    mail_to = 'erichris@live.com.mx'
    #SendInvitation(request, mail_to, 'estoesunpass2')
    #SendOnRegisterMail(request, mail_to)
    #OpenGoalMail(request, mail_to)
    SendGoalMail(request, mail_to)
    return redirect('/')

def SendGoalMail(request, email):
    html_content = render_to_string('mail_ongoals.html')
    text_content = "Gracias por ser parte de Youtube Trends #FromHome"
    subject = "Gracias por ser parte de Youtube Trends #FromHome"
    sender = settings.EMAIL_HOST_USER
    to_mail = [email]
    msg = EmailMultiAlternatives(subject, text_content,
                                 sender, to_mail)

    msg.attach_alternative(html_content, "text/html")

    msg.mixed_subtype = 'related'
    msg.send()

def OpenGoalMail(request, email):
    html_content = render_to_string('mail_open_goals.html')
    text_content = "Gracias por ser parte de Youtube Trends #FromHome"
    subject = "Seccion desbloqueada"
    sender = settings.EMAIL_HOST_USER
    to_mail = [email]
    msg = EmailMultiAlternatives(subject, text_content,
                                 sender, to_mail)

    msg.attach_alternative(html_content, "text/html")

    msg.mixed_subtype = 'related'
    msg.send()

def SendOnRegisterMail(request, email):
    html_content = render_to_string('mail_on_register.html')
    text_content = "Gracias por ser parte de Youtube Trends #FromHome"
    subject = "Gracias por ser parte de Youtube Trends #FromHome"
    sender = settings.EMAIL_HOST_USER
    to_mail = [email]
    msg = EmailMultiAlternatives(subject, text_content,
                                 sender, to_mail)

    msg.attach_alternative(html_content, "text/html")

    msg.mixed_subtype = 'related'
    msg.send()

def SendInvitation(request, email, password):
    html_content = render_to_string('mail_send_pass.html', {'User': email, 'Pass': password})
    text_content = "Te invitamos a ser parte de Youtube Trends #FromHome"
    subject = "Te invitamos a ser parte de Youtube Trends #FromHome"
    sender = settings.EMAIL_HOST_USER
    to_mail = [email]
    msg = EmailMultiAlternatives(subject, text_content,
                                 sender, to_mail)

    msg.attach_alternative(html_content, "text/html")

    msg.mixed_subtype = 'related'
    msg.send()

@csrf_exempt
def updateTalk(request):
    talk = request.POST.get('talk', None)

    platformUser = PlatformUser.objects.get(user=request.user)

    if talk == "7":
        platformUser.unlockedTalks = talk
        platformUser.save()
        OpenGoalMail(request, platformUser.user.username)
        score = request.POST.get('score', None)
        score = int(score)
        estadisticas = Estadisticas.objects.get(id=0)
        estadisticas.quizTotalesAmount += 1
        estadisticas.quizCalificationAcumulative += score
        estadisticas.save()
        if int(platformUser.quizMaxScore) < int(score):
            platformUser.quizMaxScore = score
            platformUser.save()

    if talk == "20":
        score = request.POST.get('score', None)
        score = int(score)
        estadisticas = Estadisticas.objects.get(id=0)
        estadisticas.quizTotalesAmount += 1
        estadisticas.quizCalificationAcumulative += score
        estadisticas.save()
        if int(platformUser.quizMaxScore) < int(score):
            platformUser.quizMaxScore = score
            platformUser.save()

    data = {
        'message': "Regreso exitosamente",
    }
    return JsonResponse(data)

def my_logout(request):
    if request.user != None:
        estadisticas = Estadisticas.objects.get(id=0)
        estadisticas.usuariosConectados -= 1
        if(estadisticas.usuariosConectados < 0):
            estadisticas.usuariosConectados = 0
        estadisticas.save()
    logout(request)

    return redirect('/')


def Admin_Site(request):
    if request.user.is_authenticated == False or request.user.is_staff == False:
        return redirect('/admin/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            subject = 'Invitacion a plataforma TrendsFromHome'
            message = "Username: " + form.cleaned_data.get('username') + "<br>"
            message += "Password: " + form.cleaned_data.get('password1') + "<br>"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data.get('username'), ]
            send_mail(subject, message, email_from, recipient_list, html_message=message)

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            platformUser = PlatformUser()
            platformUser.user = user
            platformUser.save()

            SendInvitation(request, form.cleaned_data.get('username'), form.cleaned_data.get('password1'))

    args = {}
    args['estadisticas'] = Estadisticas.objects.get(id="0")
    args['CreateUserForm'] = UserCreationForm()
    args['registeredUsers'] = PlatformUser.objects.count()
    args['promedioQuiz'] = args['estadisticas'].quizCalificationAcumulative / args['estadisticas'].quizTotalesAmount
    return render(request, 'charts-chartjs.html', args)

@csrf_exempt
def uploadGoal(request):
    goal = request.POST.get('goal', None)
    platformUser = PlatformUser.objects.get(user=request.user)
    platformUser.goal = goal
    platformUser.submitedGoal = datetime.now()
    platformUser.save()
    SendGoalMail(request, platformUser.user.username)
    data = {
        'message': "Regreso exitosamente",
    }
    return JsonResponse(data)

@csrf_exempt
def openVideo(request):
    estadisticas = Estadisticas.objects.get(id=0)
    platformUser = PlatformUser.objects.get(user=request.user)
    talk = request.POST.get('talk', None)
    talk = int(talk)
    estadisticas.callToAction += 1
    if talk == 1:
        estadisticas.talk1TotalReproductions += 1
        platformUser.talk1PlayTimes +=1
        platformUser.save()
    if talk == 2:
        estadisticas.talk2TotalReproductions += 1
        platformUser.talk2PlayTimes +=1
        platformUser.save()
    if talk == 3:
        estadisticas.talk3TotalReproductions += 1
        platformUser.talk3PlayTimes +=1
        platformUser.save()
    if talk == 4:
        estadisticas.talk4TotalReproductions += 1
        platformUser.talk4PlayTimes +=1
        platformUser.save()
    if talk == 5:
        estadisticas.talk5TotalReproductions += 1
        platformUser.talk5PlayTimes +=1
        platformUser.save()
    if talk == 6:
        estadisticas.talk6TotalReproductions += 1
        platformUser.talk6PlayTimes +=1
        platformUser.save()
    estadisticas.save()
    data = {
        'status_code': 0,
        'message': "Ok"
    }
    return JsonResponse(data)

@csrf_exempt
def closeVideo(request):
    talk = request.POST.get('talk', None)
    upto = request.POST.get('seconds', None)
    talk = int(talk)
    upto = float(upto)
    upto = int(upto)
    platformUser = PlatformUser.objects.get(user=request.user)
    platformUser.talk1PlayTimes += 1
    platformUser.save()
    if talk == 1:
        if platformUser.talk1UpTo < upto:
            platformUser.talk1UpTo = upto
            platformUser.save()
    if talk == 2:
        if platformUser.talk2UpTo < upto:
            platformUser.talk2UpTo = upto
            platformUser.save()
    if talk == 3:
        if platformUser.talk3UpTo < upto:
            platformUser.talk3UpTo = upto
            platformUser.save()
    if talk == 4:
        if platformUser.talk4UpTo < upto:
            platformUser.talk4UpTo = upto
            platformUser.save()
    if talk == 5:
        if platformUser.talk5UpTo < upto:
            platformUser.talk5UpTo = upto
            platformUser.save()
    if talk == 6:
        if platformUser.talk6UpTo < upto:
            platformUser.talk6UpTo = upto
            platformUser.save()
    data = {
        'status_code': 0,
        'message': "Ok"
    }
    return JsonResponse(data)


def Chart(request):
    args = {}
    args['estadisticas'] = Estadisticas.objects.get(id="0")

    args['CreateUserForm'] = UserCreationForm()

    args['registeredUsers'] = PlatformUser.objects.count()

    args['promedioQuiz'] = args['estadisticas'].quizCalificationAcumulative / args['estadisticas'].quizTotalesAmount

    return render(request, 'charts-chartjs.html', args)


@csrf_exempt
def calltoaction(request):
    print("123 this is call")
    estadisticas = Estadisticas.objects.get(id="0")
    print(estadisticas.callToAction)
    estadisticas.callToAction += 1
    print(estadisticas.callToAction)
    estadisticas.save()
    data = {
        'status_code': 0,
        'message': "Ok call"
    }
    return JsonResponse(data)

@csrf_exempt
def updateTime(request):
    estadisticas = Estadisticas.objects.get(id="0")
    estadisticas.timeInPage += 1
    estadisticas.save()
    data = {
        'status_code': 0,
        'message': "Ok time"
    }
    return JsonResponse(data)








