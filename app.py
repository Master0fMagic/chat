from flask import Flask
from flask import request
from database_controller import Database_Connector

app=Flask(__name__)
db=Database_Connector()

@app.route('/sing-in', methods=['POST'])
def sing_in():
    '''Registration
       Request: {'nickname':anyname, 'password':encoded_pass, 'registration_date':timestap_datetime}
       Response: {'id':user_id, 'status': 'OK'} if user registraition successful
       Response: {'id':0, 'status': 'This nickname is alredy been taken'} if user registraition isn`t successful'''
    req=request.get_json()
    id=db.save_new_user(req['nickname'], req['password'], req['registration_date'])
    if id is False:
        return {'id':0, 'status': 'This nickname is alredy been taken'}
    else: return {'id':id, 'status': 'OK'}

@app.route('/log-in', methods=['GET'])
def log_in():
    '''Log in
       Request: {'nickname':anyname, 'password':encoded_pass}
       Response: {'id':user_id, 'status': 'OK'} if user loged in successuful 
       Response: {'id':0, 'status': 'Wrong password or login'} if user login in isn`t successful'''
    req=request.get_json()
    id=db.log_in(req['nickname'], req['password'])
    if id is False:
        return {'id':0, 'status': 'Wrong password or login'}
    else: return {'id':id, 'status': 'OK'}

@app.route('/contacts', methods=['GET'])
def get_contacts():
    ''' Returns all nicknames
    Response: {'contacts': [nickname1, nickname2, ...]}'''
    return {'contacts':db.get_contacts()}

@app.route('/histoty', methods=['GET'])
def get_history():
    ''' Returns all messages
    Request: {'user1':nickname, 'user2':nickname}
    Response: {'messages': [{'from':nickname, 'to':nickname, 'time': timestamp_time, 'text':message}, {}, ...]}'''
    req=request.get_json()
    return db.get_messages(req['user1'], req['user2'])

@app.route('/send-message', methods=['POST'])
def save_message():
    ''' Saving message
    Request: {'from':nickname, 'to':nickname, 'time': timestamp_time, 'text':message}
    Response: {'status': 'Ok'} if saved successful or {'status':'Error'} if there are any mistake while saving'''
    req=request.get_json()
    if db.save_message(req['from'], req['to'], req['time'], req['text']):
        return {'status': 'OK'}
    else:
        return  {'status':'Error'}

@app.route('/new-messages', methods=['GET'])
def check_new_messages():
    ''' Check if there are any new messages in history
    Request: {'user1':nickname, 'user2':nickname, 'time': timestamp_time_of_last_message}
    Response: {'messages':[{'from':nickname, 'to':nickname, 'time': timestamp_time, 'text':message}, {}, ...]} 
    or {messages:[]}'''
    req=request.get_json()
    return db.get_messages(req['user1'], req['user2'], req['time'])

if __name__ == "__main__":
    app.run(port='5050')