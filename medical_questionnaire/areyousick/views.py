from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def startQuestion(request):
    
    return JsonResponse({"problem":[{"腳有傷口?":{ "actionCount": 2,"action":["是","否"]}}]})

def selectOption(request):
    
    return JsonResponse({"title" : "妥善處理傷口，並密切追蹤。","suggestion" : {"傷口護理" : ["blahblahblah..."],"感覺異常" : ["blahblahblah..."]},"isEnd" : True})

def exit(request):
    
    return JsonResponse({"isEnd" : True})