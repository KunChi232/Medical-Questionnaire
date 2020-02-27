from django.shortcuts import render
from django.http import JsonResponse
from areyousick.models import Users, Record, Symptoms
import json
import areyousick.utils as ut
# Create your views here.

def startQuestion(request):
    request = json.loads(request.body)
    print(request)
    line_id = request['line_id']
    symptoms_type = request['type']
    symptoms = Symptoms.objects.using('areyousick').filter(symptoms_type = symptoms_type)
    if(int(symptoms.count()) == 0):
        return JsonResponse({'failed':'type not found'})
    u = ut.getUser(line_id)
    if(u is False):
        u = ut.createUser(line_id)
        session = ut.createSession(u, symptoms_type)
        symptoms = Symptoms.objects.using('areyousick').filter(symptoms_type = symptoms_type)[0]
        return JsonResponse({"problem":symptoms.problem, "action":symptoms.action})
    else:
        if(ut.getSession(line_id, u.current_session).complete != 0):
            session = ut.createSession(u, symptoms_type)
            symptoms = Symptoms.objects.using('areyousick').filter(symptoms_type = symptoms_type)[0]
            return JsonResponse({"problem":symptoms.problem, "action":symptoms.action})
        else:
            return JsonResponse({'failed':'session not yet complete or exit'})

def selectOption(request):
    request = json.loads(request.body)
    print(request)
    line_id = request['line_id']
    userSelect = request['user_select']
    u = ut.getUser(line_id)
    if(u is False):
        return JsonResponse({'failed':'user not exist'})

    session = ut.getSession(line_id, u.current_session)
    if(session.complete != 0):
        return JsonResponse({'failed':'session already closed'})

    symptoms = Symptoms.objects.using('areyousick').filter(symptoms_type = session.symptoms_type)[0]
    session.complete = 1
    session.save(using = 'areyousick')
    return JsonResponse({"conclusion":json.loads(symptoms.conclusion.replace("\'", "\""))[int(userSelect)],"isEnd" : True})

def exit(request):
    request = json.loads(request.body)
    print(request)
    line_id = request['line_id']
    u = ut.getUser(line_id)
    if(u is False):
        return JsonResponse({'failed':'user not exist'})

    session = ut.getSession(line_id, u.current_session)
    if(session.complete != 0):
        return JsonResponse({'failed':'session already closed'})
    session.complete = 2
    session.save(using = 'areyousick')

    return JsonResponse({'isEnd' : True})
