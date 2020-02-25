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

    if(u is False):
        u = ut.createUser(line_id)
        session = ut.createSession(u, _type, name)
        questions = json.loads(questionnaire.questions)
        welcome = json.loads(questionnaire.wellcome)
        return JsonResponse({'questionCount' : len(questions), 'welcome': welcome[0]['params']['text'], 'sticker': welcome[1]['params']['sticker']})
    
    else:
        if(ut.getSession(line_id, u.current_session).complete != 0):
            session = ut.createSession(u, _type, name)
            questions = json.loads(questionnaire.questions)
            welcome = json.loads(questionnaire.wellcome)
            return JsonResponse({'questionCount' : len(questions), 'welcome': welcome[0]['params']['text'], 'sticker': welcome[1]['params']['sticker']})

        else:
            return JsonResponse({'failed':'session not yet complete or exit, please use getQuestion or exit api to completed'})
        
def getQuestion(request):
    request = json.loads(request.body)
    line_id = request['line_id']

    u = ut.getUser(line_id)
    if(u is False):
        return JsonResponse({'failed':'user not exist'})

    session = ut.getSession(line_id, u.current_session)
    if(session.complete != 0):
        return JsonResponse({'failed':'session already closed'})

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
    request = json.loads(request.body)
    print(request)
    line_id = request['line_id']
    user_select = request['userSelect']

    u = ut.getUser(line_id)
    if(u is False):
        return JsonResponse({'failed':'user not exist'})

    session = ut.getSession(line_id, u.current_session)
    if(session.complete != 0):
        return JsonResponse({'failed':'session already closed'})

    questionnaire = ut.getQuestionnaire(session.question_type, session.name)

    if(len(json.loads(session.user_select)) == session.next_question): 
        return JsonResponse({'failed':'you need to select question first'})

    ut.appendUserSelect(session, user_select)

    if(len(json.loads(session.user_select)) == questionnaire.question_count):
        session.complete = 1
        session.save()
        ut.calculateScore(u, session)
        return JsonResponse({'isEnd' : True})
    else:
        return JsonResponse({'isEnd' : False})

def getSummary(request):
    request = json.loads(request.body)
    line_id = request['line_id']
    u = ut.getUser(line_id)
    if(u is False):
        return JsonResponse({'failed':'user not exist'})

    session = ut.getSession(line_id, u.current_session)
    if(session.complete == 0):
        return JsonResponse({'failed':'Not yet completed, please finish whole question first'})
    questionnaire = ut.getQuestionnaire(session.question_type, session.name)

    summary = json.loads(questionnaire.summary)
    score = session.score
    summary = ut.determineSummary(score, summary)    

    if('suggest' in summary):
        suggestion = True
        suggest = summary['suggest']
    else:
        suggestion = False
        suggest = {}

    return JsonResponse({'score' : score, 'text' : ut.concateSummaryText(summary), 'sticker':summary['params']['sticker'], 'suggestion':suggestion, 'suggest':suggest})

def exit(request):
    request = json.loads(request.body)
    line_id = request['line_id']
    u = ut.getUser(line_id)
    if(u is False):
        return JsonResponse({'failed':'user not exist'})

    session = ut.getSession(line_id, u.current_session)
    if(session.complete != 0):
        return JsonResponse({'failed':'session already closed'})
    session.complete = 2
    session.save()

    return JsonResponse({'isEnd' : True})

def getScore(request):
    request = json.loads(request.body)
    line_id = request['line_id']
    u = ut.getUser(line_id)
    if(u is False):
        return JsonResponse({'failed':'user not exist'})
    return JsonResponse({'score':u.scores})