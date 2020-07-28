
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import Home, Mailing, Dashboard, Trend, Quiz, Goals, Profile, QA, Workshop, updateCont, SignUpView, validate_username, service_login, \
    service_contact, service_register, Test, updateTalk, my_logout, Admin_Site, uploadGoal, openVideo, closeVideo, Chart, calltoaction, updateTime

urlpatterns = [
    path('', Home, name = "Home"),
    path('Dashboard/', Dashboard, name = "Dashboard"),
    path('Dashboard/trend/<str:name>', Trend, name="Trend"),
    path('Quiz/', Quiz, name = "Quiz"),
    path('Goals/', Goals, name = "Goals"),
    path('Profile/', Profile, name = "Profile"),
    path('QA/', QA, name = "QA"),
    path('Workshop/', Workshop, name = "Workshop"),
    path('Dashboard/updateCont', updateCont, name="updateCont"),
    path('signup', SignUpView.as_view(), name="signup"),
    path('validate_username', validate_username, name="validate_username"),
    path('service/login', service_login, name="service_login"),
    path('service/register', service_register, name="service_register"),
    path('service/contact', service_contact, name="service_contact"),
    path('Dashboard/service/uploadGoal', uploadGoal, name="uploadGoal"),
    path('Dashboard/service/updateTalk', updateTalk, name="updateTalk"),
    path('Dashboard/service/calltoaction', calltoaction, name="calltoaction"),
    path('service/calltoaction', calltoaction, name="calltoaction"),
    path('Quiz/service/updateTalk', updateTalk, name="updateTalk"),
    path('Dashboard/service/openVideo', openVideo, name="openVideo"),
    path('Dashboard/service/closeVideo', closeVideo, name="closeVideo"),
    path('service/logout', my_logout, name="my_logout"),
    path('AdminSite/', Admin_Site, name="Admin_Site"),
    path('Chart', Chart, name="Chart"),
    path('service/logout/service/contact', service_contact, name="service_contact"),
    path('test/', Test, name="Test"),
    path('Dashboard/service/updateTime', updateTime, name="updateTime"),
    path('service/updateTime', updateTime, name="updateTime"),
]


