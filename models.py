import jwt
from dataBaseConnect import MySQLDatabase
from datetime import datetime,timedelta,timezone
class DataBase:
    def __init__(self,host,user,password,database):
        self.db = MySQLDatabase(host = host,
                                user = user,
                                password = password,
                                database = database)
    def genarete_token(self,login,secret_key,expires_in = 3600):
        payload = {
            'user_name': login,
            'exp':datetime.now(timezone.utc)+timedelta(seconds=expires_in)
        }
        return jwt.encode(payload,secret_key,algorithm='HS256')

    def registration(self,login,password,name,token="0"):
        temp = self.valid_login(login)
        if temp != 0:
            sql = f'INSERT INTO `user`(`login`, `password`, `token`, `name`) VALUES ("{login}","{password}","{token}","{name}");'
            response = self.db.execute_query(sql)
            if response == 1:
                return True
            else:
                return response
        else:
            return ('логин уже существует')
    def auth(self,login,password):
        sql = f'SELECT `name`,`token` FROM `user` WHERE login = "{login}"AND password = "{password}";'
        response = self.db.fetch_data(sql)
        token = self.genarete_token(login,password)
        if response != []:
            sql_update = f"UPDATE `user` SET `token`='{token}' WHERE `login`='{login}';"
            self.db.execute_query(sql_update)
        response = self.db.fetch_data(sql)
        return response
    def valid_login(self, login):
        sql = f"SELECT 1 FROM `user` WHERE `login`='{login}'"
        response = self.db.fetch_data(sql)
        if response != response:
            return response
        else:
            sql_update = f"UPDATE `user` SET `login`='0'"
            self.db.execute_query(sql_update)
            return ({'error':'login or token  required'}),400
    def out(self,login,token):
        sql = f'SELECT `name`,`token` FROM `user` WHERE login = "{login}" AND token = "{token}";'
        response = self.db.fetch_data(sql)
        if response != []:
            sql_update = f"UPDATE `user` SET `token`='0' WHERE `login`='{login}';"
            self.db.execute_query(sql_update)

        return 1




