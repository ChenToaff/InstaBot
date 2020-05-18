import sqlite3
from sqlite3 import Error


class Db:
    def __init__(self, path):
        self.connection = None
        try:
            self.connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        self.cursor = self.connection.cursor()

    def query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")

    def read_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def close(self):
        self.connection.close()


# example query:
def replace_table(db):
    db.query("""
    ALTER TABLE users RENAME TO tmp;
    """)
    db.query("""
    CREATE TABLE IF NOT EXISTS users (
    user_name TEXT NOT NULL PRIMARY KEY,
    following_me BIT,
    date_of_follow TEXT,
    requsted BIT,
    liked BIT,
    ignore BIT
    );""")
    db.query("""INSERT INTO users(user_name,following_me,date_of_follow,requsted,liked,ignore)
    SELECT user_name,following_me,date_of_follow,requsted,liked,ignore
    FROM tmp;
    """)
    db.query("""DROP TABLE tmp;""")


"""
INSERT INTO new_db.table_name(col1, col2) SELECT col1, col2 FROM old_db.table_name;
"""
"""
ALTER TABLE `foo` RENAME TO `bar`
"""
"""
ALTER TABLE table_name
ADD column_name datatype;
"""

"""
ALTER TABLE table_name
DROP COLUMN column_name;
"""

"""
ALTER TABLE table_name
RENAME COLUMN old_name TO new_name.
"""

select_users_posts = """
SELECT
  users.id,
  users.name,
  posts.description
FROM
  posts
  INNER JOIN users ON users.id = posts.user_id
"""
update_post_description = """
UPDATE
  posts
SET
  description = "The weather has become pleasant now"
WHERE
  id = 2
"""
delete_comment = """
DELETE FROM comments WHERE id = 5"""
