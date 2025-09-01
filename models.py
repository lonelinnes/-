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
        sql_proverka = f"SELECT * FROM `users` WHERE `login`='{login}';"
        response1 = self.db.fetch_data(sql_proverka)
        if response1 == []:
            sql = f'INSERT INTO `users`(`login`, `password`, `token`, `name`) VALUES ("{login}","{password}","{token}","{name}");'
            response = self.db.execute_query(sql)
            if response == 1:
                return True
            else:
                return response
    def auth(self,login,password):
        sql = f'SELECT `name`,`token` FROM `users` WHERE login = "{login}"AND password = "{password}";'
        response = self.db.fetch_data(sql)
        token = self.genarete_token(login,password)
        if response != []:
            sql_update = f"UPDATE `users` SET `token`='{token}' WHERE `login`='{login}';"
            self.db.execute_query(sql_update)
        response = self.db.fetch_data(sql)
        return response
    def out(self,login,token):
        sql = f'SELECT `name`,`token` FROM `users` WHERE login = "{login}" AND token = "{token}";'
        response = self.db.fetch_data(sql)
        if response != []:
            sql_update = f"UPDATE `users` SET `token`='0' WHERE `login`='{login}';"
            self.db.execute_query(sql_update)
        return 1

    def edit_password(self, login, old_pass, new_pass):
        sql = f"""
            UPDATE users 
            SET password='{new_pass}' 
            WHERE login='{login}' 
            AND password='{old_pass}'
        """
        return self.db.execute_query(sql) == 1
