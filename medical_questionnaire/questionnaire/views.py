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
    questionnaire = ut.getQuestionnaire(_type, name)

    u = ut.getUser(line_id)

    if(u is None):

        u = ut.createUser(line_id)
        session = ut.createSession(u, _type, name)
        questions = json.loads(questionnaire.questions)
        wellcome = json.loads(questionnaire.wellcome)
        return JsonResponse({'questionCount' : len(questions), 'wellcome': wellcome[0]['params']['text'], 'sticker': wellcome[1]['params']['sticker']})
    
    else:
        if(ut.getSession(line_id, u.current_session).complete != 0):
            session = ut.createSession(u, _type, name)
            questions = json.loads(questionnaire.questions)
            wellcome = json.loads(questionnaire.wellcome)
            return JsonResponse({'questionCount' : len(questions), 'wellcome': wellcome[0]['params']['text'], 'sticker': wellcome[1]['params']['sticker']})

        else:
            return JsonResponse({'failed':'session not yet complete or exit, please use getQuestion or exit api to completed'})
        
def getQuestion(request):
    request = json.loads(request.body)
    line_id = request['line_id']

    u = ut.getUser(line_id)
    session = ut.getSession(line_id, u.current_session)
    questionnaire = ut.getQuestionnaire(session.question_type, session.name)

    next_question = session.next_question

    if(next_question == questionnaire.question_count):
        return JsonResponse({'failed':'exceed question count, you need to start a new question'})

    if(len(json.loads(session.user_select)) != next_question): 
        return JsonResponse({'failed':'uesr need to select answer before getting new question'})

    questions = json.loads(questionnaire.questions)
    question = questions[next_question]

    session.next_question = next_question + 1
    session.save()

    return JsonResponse({'title' : question['params']['title'], 'text' : question['params']['text'],
                        'actionCount' : question['params']['actionCount'], "action" : ut.getActionList(question)})

def selectAnswer(request):
    pass

def getSummary(request):
    pass

def exit(request):
    pass