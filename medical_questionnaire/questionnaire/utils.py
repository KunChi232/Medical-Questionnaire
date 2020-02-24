from questionnaire.models import Users, Record, Question
import binascii, os, random
import string, secrets

def createUser(line_id):
    u = Users.objects.create(line_id = line_id, scores={}, current_session = 'None')
    u.save()
    return u

def getUser(line_id):
    u = Users.objects.filter(line_id = line_id)
    return u

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
    print(question)
    _len = len(question)
    index = random.randint(0, _len - 1)
    print(question[index].name)
    return question[index].name
