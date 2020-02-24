from django.shortcuts import render
from questionnaire.models import Users, Record, Question
from django.http import JsonResponse
import questionnaire.utils as ut
import json, ast
# Create your views here.

def startQuestion(request):
    request = json.loads(request.body)
    line_id = request['line_id']
    _type = request['type']
    name = ut.getQuestionnaireNameByType(_type)
    question = ut.getQuestionnaire(_type, name)

    u = Users.objects.filter(line_id = line_id)

    if(int(u.count()) == 0):

        u = ut.createUser(line_id)
        session = ut.createSession(u, _type, name)
        questions = ast.literal_eval(question.questions)
        wellcome = ast.literal_eval(question.wellcome)
        return JsonResponse({'questionCount' : len(question.questions), 'wellcome': wellcome[0]['params']['text'], 'sticker': wellcome[1]['params']['sticker']})
    
    else:
        u = u[0]
        if(ut.getSession(line_id, u.current_session).complete != 0):
            session = ut.createSession(u, _type, name)
            questions = ast.literal_eval(question.questions)
            wellcome = ast.literal_eval(question.wellcome)
            return JsonResponse({'questionCount' : len(questions), 'wellcome': wellcome[0]['params']['text'], 'sticker': wellcome[1]['params']['sticker']})

        else:
            return JsonResponse({'failed':'session not yet complete or exit, please use getQuestion or exit api to completed'})
        
def getQuestion(request):
    request = json.loads(request.body)
    line_id = request['line_id']
    u = ut.getUser(line_id)
    session = ut.getSession(line_id, u.current_session)
    question = ut.getQuestionnaire(session.question_type, session.name)

def selectAnswer(request):
    pass

def getSummary(request):
    pass

def exit(request):
    pass