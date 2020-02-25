"""medical_questionnaire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import questionnaire.views, areyousick.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('medical_questionnaire/questionnaire/startQuestion', questionnaire.views.startQuestion),
    path('medical_questionnaire/questionnaire/getQuestion', questionnaire.views.getQuestion),
    path('medical_questionnaire/questionnaire/selectAnswer', questionnaire.views.selectAnswer),
    path('medical_questionnaire/questionnaire/getSummary', questionnaire.views.getSummary),
    path('medical_questionnaire/questionnaire/getScore', questionnaire.views.getScore),
    path('medical_questionnaire/questionnaire/exit', questionnaire.views.exit),
    path('medical_questionnaire/areyousick/startQuestion', areyousick.views.startQuestion),
    path('medical_questionnaire/areyousick/selectOption', areyousick.views.selectOption),
    path('medical_questionnaire/areyousick/exit', areyousick.views.exit),
]
