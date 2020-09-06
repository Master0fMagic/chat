import config
import psycopg2
from datetime import datetime

class Database_Connector:
    def __init__(self):
        self.__database=config.DATABASE
        self.__user=config.USER
        self.__password=config.PASSWORD
        self.__host=config.HOST
        self.__port=config.PORT

    def save_new_user(self, nickname, password, registration_date):
        '''Take all necessary fields and saving new user to db or returns False,if that nickname is already taken or some error occured'''
        try:
            cur, con = self._open_connection()
            
            try:
                cur.execute("select id from users where nickname = %s ", (nickname,))
                rows=cur.fetchone()
                if rows is not None:
                    return False #current nickname is already taken
                cur.execute("insert into users(nickname, password, registration_time) values(%s,%s,%s) returning id;", (nickname,password,registration_date))
                id=cur.fetchone()
                return id[0]

            except:
                return False
            
            finally:
                self._close_connection(cur, con)
        
        except:
            return False
    
    def log_in(self, nickname, password):
        '''Check if login and password are correct. Return id if log in successful or False if not'''
        try:
            cur, con = self._open_connection()
            
            try:
                cur.execute('Select id from users where nickname = %s and password = %s', (nickname,password))
                id=cur.fetchone()
                if id is None:
                    return False
                return id[0]
            
            except:
                return False
            
            finally:
                self._close_connection(cur, con)

        except:
            return False

    def get_contacts(self):
        '''Returns list of contacts'''
        try:
            cur, con=self._open_connection()
            
            try:
                cur.execute('Select nickname from users order by nickname;')
                rows=cur.fetchall()
                
                if rows is None:
                    return []

                return [name[0] for name in rows]
           
            except :
                return []
            
            finally:
                self._close_connection(cur,con)
        except:
            return []

    def save_message(self, from_user, to_user, timestamp_time, text):
        '''Save new message in db. 
        Returns True if saving successful or False, if not'''
        try:
            cur, con=self._open_connection()
            
            try:
                cur.execute('insert into messages("from", "to", "text", "send_time") values(%s, %s, %s, %s );', (from_user, to_user, text, timestamp_time))
                return True
           
            except Exception as e:
                print(f'Exception: {e}')
                return False
            
            finally:
                self._close_connection(cur,con)
        except:
            return False

    def get_messages(self, nickname1, nickname2, time=0):
        '''If time is 0, returns all messages of the 2 users if they exist or False if not
        If time isn`t 0, returns all messages after time if they exist or False if not
        returning format: {'messages': [{'from':nickname, 'to':nickname, 'time': timestamp_time, 'text':message}, {}, ...]}'''
        result={'messages':[]}
        try:
            cur, con=self._open_connection()
            
            try:
                cur.execute('Select "from", "to", "send_time", "text" from messages where (("from" =%s and "to" = %s) or ("from" =%s and "to" = %s)) and "send_time" > %s order by "send_time" ASC;', (nickname1, nickname2, nickname2, nickname1, time))
                rows=cur.fetchall()
                if rows is None:
                    return result
               
                for row in rows:
                    result['messages'].append({'from':row[0], 'to':row[1], 'send_time':float(row[2]), 'text':row[3]})
                return result

            except:
                return result
            
            finally:
                self._close_connection(cur,con)
        except:
            return result

    def _open_connection(self):
        ''' Opens db connection. Returns cursor and connection'''
        con=psycopg2.connect(database=self.__database, user=self.__user, password=self.__password, host=self.__host, port=self.__port)
        cur=con.cursor()
        return cur,con

    def _close_connection(self,cur,con):
        con.commit()
        cur.close()
        con.close()
            
