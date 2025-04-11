import mysql.connector
from mysql.connector import Error
class MySQLDatabase:
    '''Класс для подключения и работы с базой данных'''
    def __init__(self,host,user,password,database):
        try:
            self.connection = mysql.connector.connect(
                host = host,
                user = user,
                password = password,
                database = database
            )
            self.cursor = self.connection.cursor()
            print(f'Connect db {database} complite')
        except Error as e:
            print(f'Ошибка подключения к MySQL: {e}')
    def execute_query(self,query,params = None):
        '''отправляет запросы в базу'''
        try:
            self.cursor.execute(query,params or ())
            self.connection.commit()
            return True
        except Error as e:
            return e
    def fetch_data(self,query,params = None):
        '''Получает данные из базы'''
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Ошибка получения данных: {e}")
            return None
    def close(self):
        '''Закрытие подключения'''
        if self.connection.is_connected():
            self.cursor.close()
            self.connection()
            print("Подключение к MySQL закрыто")




