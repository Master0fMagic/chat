from datetime import datetime
import requests

class User:
    def __init__(self, nickname, password, registration_date):
        self.nickname=nickname
        self.password=password
        self.__id=None
        self.registration_date=registration_date

    def is_valid_id(self):
        ''' Returnes True if id exists, False, if id isn`t exist'''
        return self.__id != None

    def save_new_user(self):
        ''' Saving new user to DB. This method sets User`s id '''
        try:
            r=requests.post('http://127.0.0.1:5050/sing-in', json=self.__to_json())
            r=r.json()
            if r['status'] == 'OK':
                self.__id=r['id']
                return True
            return False
        except:
            return False

    def check_user(self ):
        ''' Check if this user is exist and if password is correct. If user exists and password is correct, method sets id. '''
        try:
            r=requests.get('http://127.0.0.1:5050/log-in', json={'nickname':self.nickname, 'password':self.password})
            r=r.json()
            if r['status'] == 'OK':
                self.__id=r['id']
                return True
            return False
        except:
            return False

    def get_contacts(self):
        ''' Returns list of users which are loged into chat '''
        try:
            r=requests.get('http://127.0.0.1:5050//contacts')
            r=r.json()
            return r['contacts']
        except:
            return []

    def get_message_history(self,nickname):
        ''' Returns list of all current user`s and nickname`s messages '''
        result = []
        try:
            r=requests.get('http://127.0.0.1:5050/histoty', json={'user1':self.nickname, 'user2':nickname})
            r=r.json()
            for message in r['messages']:
                result.append(Message(message['from'], message['to'], message['text'],message['send_time']))
            return result
        except:
            return result
            
    def send_message(self, message):
        ''' Takes an object of Message. Sends the message and saving it to history '''
        try:
            r=requests.post('http://127.0.0.1:5050/send-message', json=message.to_json())
            r=r.json()
            if r['status'] == 'OK':
                return True
            else:
                return False
        except:
            return False

    def check_new_message(self, message):
        ''' Takes an object of the last message, that have been showed already. '''
        result = []
        try:
            r=requests.get('http://127.0.0.1:5050/new-messages', json={'user1':message.user_from, 'user2':message.user_to, 'time':message.time})
            r=r.json()
            for message in r['messages']:
                result.append(Message(message['from'], message['to'], message['text'],message['send_time']))
            return result
        except:
            return result

    def __to_json(self):
        ''' Returnes value in JSON type to be able send user through http request'''
        return { 'nickname':self.nickname, 'password':self.password, 'registration_date':self.registration_date}

class Message:
    def __init__(self, user_from, user_to, text, time=None):
        self.user_from=user_from
        self.user_to=user_to
        self.text=text
        if time is None:
            self.time=datetime.now().timestamp()
        else:
            self.time=time

    def to_json(self):
        ''' Returnes value in JSON type to be able send message through http request'''
        return {'from':self.user_from, 'to':self.user_to, 'time':self.time, 'text':self.text}

    def to_str(self):
        '''Return a message in string format'''
        return f'{self.user_from} {datetime.fromtimestamp(self.time).strftime("%d.%m.%Y at %H:%M:%S")}: {self.text}\n'

    def __repr__(self):
        return f'{self.user_from} to {self.user_to} {datetime.fromtimestamp(self.time).strftime("%d.%m.%Y at %H:%M:%S")}: {self.text}\n'

