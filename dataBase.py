from sqlite3 import Error,connect

class Db:
    def __init__(self, path):
        self.connection = None
        try:
            self.connection = connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        self.cursor = self.connection.cursor()

    def query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        

    def read_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def close(self):
        self.connection.close()


