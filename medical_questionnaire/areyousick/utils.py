from areyousick.models import Users, Symptoms, Record
import secrets

def createUser(line_id):
    u = Users.objects.using('areyousick').create(line_id = line_id, current_session = 'None')
    u.save(using='areyousick')
    return u

def getUser(line_id):
    u = Users.objects.using('areyousick').filter(line_id = line_id)
    if(u.count() == 0):
        return False
    return u[0]

def createSession(u, symptoms_type):
    randomHash = secrets.token_hex(nbytes=16)
    u.current_session = randomHash
    u.save()
    session = Record.objects.using('areyousick').create(line_id = str(u.line_id), session_id = str(u.current_session), symptoms_type = symptoms_type, complete = 0)
    session.save(using='areyousick')
    return session

def getSession(line_id, session_id):
    session = Record.objects.using('areyousick').filter(line_id = line_id, session_id = session_id)
    return session[0]