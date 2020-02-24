from questionnaire.models import Users, Record, Question
import binascii, os, random, json
import string, secrets
from django.http import JsonResponse

def createUser(line_id):
    u = Users.objects.create(line_id = line_id, scores={}, current_session = 'None')
    u.save()
    return u

def getUser(line_id):
    u = Users.objects.filter(line_id = line_id)
    if(u.count() == 0):
        return False
    return u[0]

def createSession(u, _type, name):
    randomHash = secrets.token_hex(nbytes=16)
    u.current_session = randomHash
    u.save()
    session = Record.objects.create(line_id = str(u.line_id), session_id = str(u.current_session), question_type = str(_type), 
                                    name = str(name), user_select = str([]), next_question = 0, complete = 0)
    session.save()
    return session

def getSession(line_id, session_id):
    session = Record.objects.filter(line_id = line_id, session_id = session_id)
    return session[0]

def getQuestionnaire(_type, name):
    question = Question.objects.filter(question_type = _type, name = name)
    return question[0]

def getQuestionnaireNameByType(_type):
    question = Question.objects.filter(question_type = _type)
    _len = len(question)
    index = random.randint(0, _len - 1)
    return question[index].name

def getActionList(question):
    actions = []
    for i in range(question['params']['actionCount']):
        actions.append(question['params']['actions.'+str(i)]['text'])
    return actions

def appendUserSelect(session, user_select):

    select_list = json.loads(session.user_select)
    select_list.append(user_select)
    session.user_select = str(select_list)
    session.save()

    

def calculateScore(u, session):

    def appendScore(u, _type, name, score):
        u_score = json.loads(u.scores)
        if(_type not in u_score):
            u_score[_type] = {}
        u_score[_type][name] = score
        u.scores = str(u_score).replace('\'', '\"')
        u.save()

    score = sum(json.loads(session.user_select))
    session.score = score
    session.save()
    return appendScore(u, session.question_type, session.name, score)

