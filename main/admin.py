from django.contrib import admin

# Register your models here.
from .models import PlatformUser, SpeakersSection, Question, Talks, Trends, Estadisticas

admin.site.register(PlatformUser)
admin.site.register(Question)
admin.site.register(Trends)
admin.site.register(Estadisticas)